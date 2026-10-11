"""Definicao dos algoritmos de classificacao e montagem do pipeline completo sem vazamento.

Arquivo base (stub) para implementacao da Etapa 3 pela equipe.
"""

from typing import Any, Dict, Literal, Optional
from src.config import RANDOM_STATE


def get_classifier(
    model_name: Literal["decision_tree", "random_forest", "mlp", "hist_gradient_boosting", "logistic_regression"],
    params: Optional[Dict[str, Any]] = None,
    random_state: int = RANDOM_STATE,
) -> Any:
    """
    Instancia e configura um classificador com parametros para experimentacao.

    Requisito do enunciado (Etapa 3):
    - Testar no minimo 3 algoritmos de classificacao diferentes dentre os vistos na disciplina.
      Exemplos sugeridos:
      1. 'decision_tree': DecisionTreeClassifier (interpretavel, rapida).
      2. 'random_forest': RandomForestClassifier (ensemble baseado em bagging, robusto a variancia).
      3. 'mlp': MLPClassifier (Rede Neural Multicamadas / Perceptron).

    Parametros:
    - model_name: Nome do algoritmo escolhido.
    - params: Dicionario opcional de hiperparametros para sobrescrever os padroes.
    - random_state: Semente para garantir resultados reproduziveis.

    Retorno:
    - Estimador compativel com o Scikit-Learn.
    """
    # TODO: Implementar a instanciacao dos 3 modelos obrigatorios (Decision Tree, Random Forest, MLP)
    raise NotImplementedError("TODO: Implementar funcao get_classifier")


def build_pipeline(
    preprocessor: Any,
    sampler: Optional[Any],
    classifier: Any,
) -> Any:
    """
    Constroi uma pipeline unificada (usando imblearn.pipeline.Pipeline).

    PREVENCAO DE DATA LEAKAGE:
    - Se sampler for fornecido, a pipeline DEVE ser do imblearn para que o sampler
      atue somente nas dobras de treino durante a validacao cruzada.
    - Se sampler for None, encadeia apenas [('preprocessor', preprocessor), ('classifier', classifier)].

    Parametros:
    - preprocessor: Pipeline ou ColumnTransformer de pre-processamento.
    - sampler: Estimador de reamostragem do imblearn ou None.
    - classifier: Estimador do modelo de classificacao.

    Retorno:
    - Pipeline executavel.
    """
    # TODO: Implementar a montagem da Pipeline do imblearn encadeando os passos
    raise NotImplementedError("TODO: Implementar funcao build_pipeline")
