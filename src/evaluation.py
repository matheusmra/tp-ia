"""Avaliacao dos modelos por validacao cruzada e teste final com foco na metrica oficial F1-macro.

Arquivo base (stub) para implementacao das Etapas 3 e 4 pela equipe.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from src.config import CLASSES_5, FIGURES_DIR, RANDOM_STATE


def evaluate_cross_validation(
    pipeline: Any,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_splits: int = 5,
    random_state: int = RANDOM_STATE,
) -> Dict[str, Any]:
    """
    Executa validacao cruzada estratificada (StratifiedKFold) sem vazamento de dados.

    Como a pipeline e gerenciada pelo imblearn/sklearn, a cada particao (fold):
    - O pre-processamento e o balanceamento devem ser ajustados exclusivamente na particao de treino do fold.
    - A particao de validacao e apenas transformada e avaliada.

    Metricas a calcular:
    - F1-macro (media e desvio padrao entre os folds) - METRICA OFICIAL DA COMPETICAO
    - Acuracia media e desvio padrao
    - Tempo total de execucao

    Parametros:
    - pipeline: Pipeline contendo pre-processador, sampler (opcional) e classificador.
    - X_train: DataFrame com atributos descritivos do conjunto de treino.
    - y_train: Series com os rotulos das 5 superclasses.
    - n_splits: Quantidade de folds na validacao cruzada.
    - random_state: Semente para embaralhamento reproduzivel das particoes.

    Retorno:
    - Dicionario com as metricas calculadas.
    """
    # TODO: Implementar StratifiedKFold e calculo das metricas por fold
    raise NotImplementedError("TODO: Implementar funcao evaluate_cross_validation")


def evaluate_on_test_set(
    pipeline: Any,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Dict[str, Any]:
    """
    Avaliacao final estrita no conjunto de teste (KDDTest+) para a Etapa 4.

    IMPORTANTE (Regra da competicao):
    - O arquivo KDDTest+ so pode ser utilizado nesta avaliacao final.
    - O pipeline e ajustado no KDDTrain+ completo e prediz sobre o KDDTest+.

    Metricas:
    - F1-macro oficial do ranking
    - Matriz de confusao
    - Relatorio de classificacao por classe (classification_report)

    Retorno:
    - Dicionario com os resultados finais no teste.
    """
    # TODO: Ajustar pipeline em KDDTrain+, predizer em KDDTest+ e calcular metricas finais
    raise NotImplementedError("TODO: Implementar funcao evaluate_on_test_set")


def plot_and_save_confusion_matrix(
    cm: np.ndarray,
    labels: List[str] = CLASSES_5,
    title: str = "Matriz de Confusao - Avaliacao Final",
    filename: str = "matriz_confusao.png",
) -> str:
    """
    Gera o mapa de calor (heatmap) da matriz de confusao e salva na pasta reports/figures.
    """
    # TODO: Implementar geracao visual da matriz de confusao com seaborn/matplotlib
    raise NotImplementedError("TODO: Implementar funcao plot_and_save_confusion_matrix")


def build_comparison_table(results_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Formata os resultados dos experimentos na tabela comparativa exigida pelo enunciado:
    (estrategia de pre-processamento x algoritmo x metricas).
    """
    # TODO: Consolidar lista de dicionarios em um DataFrame estruturado
    raise NotImplementedError("TODO: Implementar funcao build_comparison_table")
