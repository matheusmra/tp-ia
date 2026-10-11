# Estrutura do Relatorio Final (3 a 5 paginas)
## Disciplina: Inteligencia Artificial
### Professora: Cristiane Neri Nobre
### Trabalho em Competicao: Deteccao de Intrusao em Redes (NSL-KDD)

---

## 1. Introducao e Contexto do Problema
- Breve descricao do problema de deteccao de intrusao em redes de computadores.
- Caracterizacao da base NSL-KDD (41 features descritivas, distribuicao desbalanceada das classes, conjunto de treino KDDTrain+ e teste KDDTest+).
- Definicao da metrica de avaliacao oficial da competicao: F1-score macro.

## 2. Metodologia e Cuidados contra Vazamento de Dados (Data Leakage)
- Explicacao do isolamento metodologico rigoroso do conjunto de teste (KDDTest+), utilizado exclusivamente na avaliacao final.
- Justificativa para a remocao do atributo `difficulty_level` das features descritivas (metrica auxiliar externa que nao compoe o trafego de rede).
- Tratamento de atributos redundantes/constantes (exclusao de `num_outbound_cmds` devido a variancia zero).
- Estruturacao do pipeline com `imblearn.pipeline.Pipeline`, garantindo que balanceamento (SMOTE/RandomUnderSampler) e transformacoes (scalers, encoders) sejam ajustados apenas no conjunto de treino de cada particao da validacao cruzada.

## 3. Experimentos de Pre-Processamento e Justificativas Tecnicas
### 3.1 Tratamento de Inconsistencias e Redundancias
- Analise das duplicatas parciais e decisoes tomadas.

### 3.2 Conversao Simbolico-Numerica
- Discussao da alta cardinalidade do atributo `service` (mais de 65 categorias unicas).
- Comparativo tecnico entre One-Hot Encoding e Frequency/Count Encoding (ou Ordinal/Target Encoding).

### 3.3 Normalizacao e Transformacao Numerica
- Comparativo entre `StandardScaler` e `RobustScaler` (sensibilidade a outliers no trafego de pacotes).

### 3.4 Reducao de Dimensionalidade ou Selecao de Atributos
- Justificativa da tecnica adotada (ex.: selecao univariada via `SelectKBest` ou projecao via `PCA`).

### 3.5 Tecnicas de Balanceamento de Classes
- Comparacao tecnica entre tecnicas testadas (ex.: SMOTE vs. RandomUnderSampler vs. Baseline).
- Impacto do desbalanceamento severo, principalmente sobre as classes minoritarias `u2r` e `r2l`.

## 4. Algoritmos de Classificacao e Tabela Comparativa Estruturada
### 4.1 Descricao dos Classificadores
- Arvore de Decisao (Decision Tree)
- Random Forest
- Perceptron Multicamadas (MLP)

### 4.2 Tabela Comparativa das Combinacoes Testadas
| ID | Estrategia de Pre-Processamento | Balanceamento | Algoritmo | F1-Macro (CV) | F1-Macro Desvio Padrao | Acuracia (CV) |
|---|---|---|---|---|---|---|
| E1 | One-Hot + StandardScaler | Nenhum | Decision Tree | - | - | - |
| E2 | One-Hot + StandardScaler | SMOTE | Decision Tree | - | - | - |
| E3 | Frequency + RobustScaler | SMOTE | Random Forest | - | - | - |
| E4 | Frequency + RobustScaler | RandomUnderSampler | Random Forest | - | - | - |
| E5 | Frequency + RobustScaler | SMOTE | MLP | - | - | - |

### 4.3 Discussao dos Resultados
- Analise dos compromissos entre precisao e revocacao nas classes raras.
- Justificativa tecnica para a escolha da combinacao vencedora.

## 5. Avaliacao Final no Conjunto de Teste (KDDTest+) e Explicabilidade
- Resultado oficial obtido no conjunto de teste: F1-score macro.
- Matriz de confusao e diagnostico do comportamento do modelo frente aos novos ataques (novel attacks presentes apenas no teste).
- Explicabilidade do modelo vencedor: analise de importancia de atributos (Feature Importances / SHAP) e correlacao com o dominio de seguranca.

## 6. Conclusao
- Sintese dos principais achados tecnicos e licoes metodologicas.

## 7. Declaracao de Integridade Academica e Uso de Ferramentas
- Declaracao de autoria do trabalho.
- Descricao do uso de eventuais ferramentas de IA generativa para auxilio na codificacao ou estruturacao textual, indicando ferramenta e finalidade (conforme item 8 do enunciado).
