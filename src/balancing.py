"""Modulo de balanceamento de classes com tecnicas do imblearn.

Arquivo base (stub) para implementacao da Etapa 2 pela equipe.
"""

from typing import Literal, Optional, Union
from src.config import RANDOM_STATE


def get_sampler(
    sampler_type: Literal["none", "smote", "random_undersampler", "borderline_smote"] = "smote",
    sampling_strategy: Union[str, dict] = "auto",
    k_neighbors: int = 5,
    random_state: int = RANDOM_STATE,
) -> Optional[object]:
    """
    Retorna o estimador de balanceamento configurado conforme as tecnicas exigidas no enunciado.

    Requisito do enunciado:
    - Comparar pelo menos 2 tecnicas de balanceamento de classes (ex.: SMOTE vs. RandomUnderSampler).

    REGRA METODOLOGICA CONTRA DATA LEAKAGE (30% da avaliacao):
    - O estimador retornado por esta funcao deve ser inserido em uma 'imblearn.pipeline.Pipeline'.
    - O balanceamento NUNCA deve ser aplicado na base inteira antes da validacao cruzada ou no conjunto de teste.
    - O re-sampling deve atuar estritamente dentro da particao de treino de cada dobra.

    Estrategias sugeridas:
    - 'none': Retorna None (baseline sem balanceamento).
    - 'smote': Superamostragem sintetica (SMOTE do imblearn.over_sampling).
    - 'random_undersampler': Subamostragem aleatoria (RandomUnderSampler do imblearn.under_sampling).
    - 'borderline_smote': Superamostragem nas fronteiras de decisao (BorderlineSMOTE).

    Parametros:
    - sampler_type: Nome da tecnica a instanciar.
    - sampling_strategy: Estrategia de reamostragem (ex.: 'auto', dicionario ou fracao).
    - k_neighbors: Quantidade de vizinhos mais proximos para metodos baseados em SMOTE.
    - random_state: Semente pseudoaleatoria para reprodutibilidade.

    Retorno:
    - Estimador compativel com o imblearn ou None.
    """
    # TODO: Implementar a instanciacao dos samplers do imblearn
    raise NotImplementedError("TODO: Implementar funcao get_sampler")
