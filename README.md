# Competicao de Inteligencia Artificial: Deteccao de Intrusao em Redes

Projeto desenvolvido para a disciplina de Inteligencia Artificial (Professora: Cristiane Neri Nobre).
O objetivo do trabalho e aplicar etapas de pre-processamento de dados de forma critica e fundamentada na base de dados **NSL-KDD**, comparando classificadores com foco na metrica oficial **F1-score macro** e garantindo rigor metodologico contra vazamento de dados (**data leakage**).

---

## Estrutura do Projeto

```text
tp-ia/
├── data/
│   ├── raw/                              # Arquivos brutos originais (KDDTrain+.txt, KDDTest+.txt)
│   └── processed/                        # Dados intermediarios ou caches (se necessario)
├── notebooks/
│   ├── 01_analise_exploratoria.ipynb     # Etapa 1: EDA, desbalanceamento, qualidade e leakage
│   ├── 02_pre_processamento.ipynb        # Etapa 2: Experimentos comparativos de pre-processamento
│   ├── 03_classificadores.ipynb          # Etapa 3: Treinamento, validacao cruzada e tabela comparativa
│   └── 04_avaliacao_final.ipynb          # Etapa 4: Avaliacao em KDDTest+ e explicabilidade
├── src/                                  # Codigo modular compartilhado (sem duplicacao e sem leakage)
│   ├── __init__.py
│   ├── config.py                         # Constantes, caminhos, nomes das 43 colunas e mapeamentos
│   ├── data_loader.py                    # Carga de dados, remocao de difficulty_level e checagem de qualidade
│   ├── preprocessing.py                  # ColumnTransformer modular (OneHot, Frequency, scalers, selecao)
│   ├── balancing.py                      # Balanceamento com imblearn (SMOTE, RandomUnderSampler)
│   ├── models.py                         # Construtor dos algoritmos (Decision Tree, Random Forest, MLP)
│   └── evaluation.py                     # StratifiedKFold sem vazamento, metricas e matriz de confusao
├── reports/
│   ├── figures/                          # Graficos gerados para o relatorio
│   └── estrutura_relatorio.md            # Template estruturado para o relatorio final (3 a 5 paginas)
├── requirements.txt                      # Dependencias Python necessarias
├── .gitignore                            # Arquivos e diretorios ignorados pelo git
└── README.md                             # Documentacao do projeto
```

---

## Requisitos e Instalacao

Recomenda-se o uso de um ambiente virtual Python (versao 3.10 ou superior).

1. Crie e ative o ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependencias:
```bash
pip install -r requirements.txt
```

---

## Modulos Base (src/)

- **`config.py`**: Centraliza os caminhos do projeto, a semente aleatoria (`RANDOM_STATE = 42`), as listas de features numericas e categoricas, o atributo `difficulty_level`, e o dicionario completo `ATTACK_MAPPING` que converte os 40 tipos de ataque observados em treino e teste para as 5 superclasses canonicas: `normal`, `dos`, `probe`, `r2l` e `u2r`.
- **`data_loader.py`**: Carrega `KDDTrain+.txt` e `KDDTest+`. Por padrao, separa `X` e `y`, mapeia as classes, remove o atributo `difficulty_level` (para evitar vazamento) e elimina colunas de variancia zero como `num_outbound_cmds`.
- **`preprocessing.py`**: Construtor flexivel de `ColumnTransformer` compativel com o Scikit-Learn. Oferece codificacao One-Hot tradicional e Frequency/Count Encoding para o atributo `service` (devido a sua alta cardinalidade com mais de 65 servicos), alem de selecao univariada (`SelectKBest`) ou projecao (`PCA`).
- **`balancing.py`**: Fabrica de estimadores de balanceamento com `imblearn` (`SMOTE`, `RandomUnderSampler`).
- **`models.py`**: Fabrica de classificadores (`DecisionTreeClassifier`, `RandomForestClassifier`, `MLPClassifier`) e construtor de pipelines unificadas via `imblearn.pipeline.Pipeline`.
- **`evaluation.py`**: Utilitarios de validacao cruzada estratificada (`StratifiedKFold`) onde transformacoes e amostragem ocorrem apenas na particao de treino de cada dobra, funcao para avaliacao final em `KDDTest+` e geracao da matriz de confusao.

---

## Pontos de Controle do Cronograma

| Etapa | Data | Atividades | Entregavel |
|---|---|---|---|
| **1. Analise Exploratoria** | 24/10 | Caracterizacao da base, distribuicao de classes, desbalanceamento severo (ex.: U2R), categoricos, variancia zero e diagnostico de data leakage. | `notebooks/01_analise_exploratoria.ipynb` |
| **2. Pre-Processamento** | 07/11 | Comparacao de 2 balanceamentos (SMOTE vs RandomUnderSampler), 1 codificacao categorica (OneHot vs Frequency para service), 1 normalizacao e 1 reducao/selecao. | `notebooks/02_pre_processamento.ipynb` |
| **3. Classificadores** | 21/11 | Treinamento dos 3 algoritmos, comparacao de combinacoes em validacao cruzada estratificada e tabela comparativa. | `notebooks/03_classificadores.ipynb` |
| **4. Competicao Final** | 28/11 | Avaliacao definitiva no KDDTest+, calculo oficial do F1-macro, explicabilidade (SHAP / Feature Importances) e relatorio final de 3 a 5 paginas. | `notebooks/04_avaliacao_final.ipynb` e `reports/` |

---

## Prevencao Metodologica contra Data Leakage

1. **Uso exclusivo do conjunto de teste**: O arquivo `KDDTest+.txt` deve ser utilizado unicamente na etapa final. Todas as decisoes de preprocessamento, selecao de atributos e ajuste de hiperparametros devem ser validadas apenas no `KDDTrain+`.
2. **Remocao de `difficulty_level`**: Esse atributo presente no arquivo bruto e uma estimativa de dificuldade de predicao externa ao trafego de rede. Inclui-lo nas features preditivas constitui vazamento direto de informacao.
3. **Pipeline integrada**: Todo balanceamento (`SMOTE`, `RandomUnderSampler`) e escalonamento (`StandardScaler`, `RobustScaler`) deve ser executado dentro da `Pipeline` do `imblearn`, garantindo que o ajuste (`fit`) ocorra exclusivamente sobre o subconjunto de treino da particao.
