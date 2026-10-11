"""Transformadores e construtores de pipelines de pre-processamento compativeis com scikit-learn.

Arquivo base (stub) para implementacao da Etapa 2 pela equipe.
"""

from typing import List, Literal, Optional, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class FrequencyEncoder(BaseEstimator, TransformerMixin):
    """
    Transformador de codificacao por frequencia (Frequency/Count Encoding).

    Substitui categorias pela sua frequencia relativa observada no conjunto de treino.
    Recomendado para atributos de alta cardinalidade como 'service' (mais de 65 categorias no NSL-KDD),
    evitando a explosao da dimensionalidade e a esparsidade geradas pelo One-Hot Encoding puro.

    Atencao metodologica contra Data Leakage:
    - O calculo das frequencias deve ocorrer exclusivamente durante o metodo fit (com dados de treino).
    - Categorias presentes no teste mas ausentes no treino devem receber frequencia 0.0 no transform.
    """

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns
        self.frequencies_: dict = {}

    def fit(self, X: Union[pd.DataFrame, np.ndarray], y=None):
        """
        Calcula as frequencias relativas das categorias de cada coluna no conjunto de treino.
        """
        # TODO: Implementar o ajuste das frequencias relativas por coluna
        raise NotImplementedError("TODO: Implementar metodo fit do FrequencyEncoder")

    def transform(self, X: Union[pd.DataFrame, np.ndarray]) -> Union[pd.DataFrame, np.ndarray]:
        """
        Mapeia as categorias para as frequencias relativas calculadas no treino.
        """
        # TODO: Implementar a transformacao substituindo categorias pelas frequencias
        raise NotImplementedError("TODO: Implementar metodo transform do FrequencyEncoder")


def build_preprocessor(
    categorical_strategy: Literal["onehot", "frequency_service", "ordinal"] = "onehot",
    scaler_type: Literal["standard", "robust", "minmax", "none"] = "standard",
    feature_reduction: Literal["none", "select_k_best", "pca"] = "none",
    n_features_or_components: int = 25,
    feature_columns: Optional[List[str]] = None,
) -> Pipeline:
    """
    Constroi o pipeline modular de pre-processamento com ColumnTransformer e selecao/reducao.

    Requisitos do enunciado (Etapa 2):
    1. Codificacao simbolico-numerica (avaliar efeito da alta cardinalidade de 'service').
    2. Normalizacao/transformacao de atributos numericos (StandardScaler vs. RobustScaler).
    3. Reducao de dimensionalidade ou selecao de atributos (PCA vs. SelectKBest).

    Parametros:
    - categorical_strategy:
        'onehot': OneHotEncoder com handle_unknown='ignore'.
        'frequency_service': OneHot para protocol_type e flag, e FrequencyEncoder para service.
        'ordinal': OrdinalEncoder com tratamento de desconhecidos.
    - scaler_type:
        'standard': StandardScaler.
        'robust': RobustScaler (resistente a outliers de trafego).
        'minmax': MinMaxScaler.
        'none': Sem escalonamento.
    - feature_reduction:
        'none': Mantem todas as features.
        'select_k_best': Selecao univariada supervisionada (SelectKBest).
        'pca': Projecao nao-supervisionada em componentes principais (PCA).
    - n_features_or_components: Quantidade de features/componentes selecionados.
    - feature_columns: Lista de nomes de colunas do DataFrame X de entrada.

    Retorno:
    - Pipeline ou ColumnTransformer compativel com o Scikit-Learn.
    """
    # TODO: Implementar os transformadores categoricos (OneHot / Frequency)
    # TODO: Implementar os transformadores numericos (Standard / Robust / MinMaxScaler)
    # TODO: Montar o ColumnTransformer combinando os grupos de atributos
    # TODO: Acoplar a etapa de reducao/selecao de atributos se feature_reduction != 'none'
    raise NotImplementedError("TODO: Implementar funcao build_preprocessor")
