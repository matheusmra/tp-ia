"""Carregamento e preparacao dos conjuntos KDDTrain+ e KDDTest+."""

from pathlib import Path
from typing import Optional, Tuple
import pandas as pd

from src.config import (
    ALL_COLUMNS,
    ATTACK_MAPPING,
    DATA_DIR,
    DIFFICULTY_NAME,
    LABEL_NAME,
    RAW_DATA_DIR,
    ZERO_VARIANCE_FEATURES,
)


def resolve_data_path(filename: str) -> Path:
    """Localiza o arquivo no diretorio raw ou na raiz de data."""
    path_raw = RAW_DATA_DIR / filename
    if path_raw.exists():
        return path_raw

    path_data = DATA_DIR / filename
    if path_data.exists():
        return path_data

    raise FileNotFoundError(
        f"Arquivo {filename} nao encontrado em {RAW_DATA_DIR} nem em {DATA_DIR}."
    )


def load_raw_dataframe(split: str = "train") -> pd.DataFrame:
    """Carrega o DataFrame bruto com todas as 43 colunas originais."""
    if split == "train":
        filepath = resolve_data_path("KDDTrain+.txt")
    elif split == "test":
        filepath = resolve_data_path("KDDTest+.txt")
    else:
        raise ValueError("O parametro split deve ser 'train' ou 'test'.")

    df = pd.read_csv(filepath, header=None, names=ALL_COLUMNS)
    return df


def prepare_dataset(
    split: str = "train",
    map_to_5_classes: bool = True,
    drop_difficulty: bool = True,
    drop_zero_variance: bool = True,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Carrega o dataset e separa as features descritivas (X) do rotulo (y).

    Aspectos de seguranca metodologica contra Data Leakage:
    - O atributo 'difficulty_level' e removido de X por padrao para evitar vazamento.
    - O mapeamento para as 5 superclasses (normal, dos, probe, r2l, u2r) e aplicado ao rotulo.
    - O split fornecido pela base e estritamente respeitado.
    """
    df = load_raw_dataframe(split=split)

    if map_to_5_classes:
        y = df[LABEL_NAME].map(ATTACK_MAPPING)
        unmapped_count = y.isna().sum()
        if unmapped_count > 0:
            raise ValueError(f"Existem {unmapped_count} rotulos sem mapeamento!")
    else:
        y = df[LABEL_NAME].copy()

    cols_to_drop = [LABEL_NAME]

    if drop_difficulty:
        cols_to_drop.append(DIFFICULTY_NAME)

    if drop_zero_variance:
        cols_to_drop.extend([col for col in ZERO_VARIANCE_FEATURES if col in df.columns])

    X = df.drop(columns=cols_to_drop)

    return X, y


def load_train_and_test(
    map_to_5_classes: bool = True,
    drop_difficulty: bool = True,
    drop_zero_variance: bool = True,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """Carrega ambos os conjuntos de treino e teste preparados para os experimentos."""
    X_train, y_train = prepare_dataset(
        split="train",
        map_to_5_classes=map_to_5_classes,
        drop_difficulty=drop_difficulty,
        drop_zero_variance=drop_zero_variance,
    )
    X_test, y_test = prepare_dataset(
        split="test",
        map_to_5_classes=map_to_5_classes,
        drop_difficulty=drop_difficulty,
        drop_zero_variance=drop_zero_variance,
    )
    return X_train, y_train, X_test, y_test
