# Detecção de intrusão em redes: relatório final

**Inteligência Artificial · Profa. Cristiane Neri Nobre · Grupo 10 · 28/11/2026**

**Integrantes:** Arthur Soares Rolla, Carlos Eduardo de Melo Sabino, Matheus de Almeida Moreira, Paulo Gabriel de Oliveira Leite e Samuel Lucas Rodrigues Vieira.

> **Antes do envio (apagar este bloco):** (1) restaurar a célula SHAP do Membro 3 no notebook 04 e executar *Restart & Run All*; (2) conferir os números da seção 5 com a ficha da entrega (notebook 04, seção 5.2) e os da seção 6 com a seção 3 do notebook 04; (3) confirmar a tabela de contribuições da seção 8: o cabeçalho do notebook 02 atribui a codificação a Carlos Eduardo e o PCA a Arthur, mas o histórico de commits indica o contrário; (4) confirmar as ferramentas de IA usadas pelos membros 3 e 4 na etapa 4; (5) exportar para PDF e conferir se ficou entre 3 e 5 páginas.

## 1. Problema, dados e métrica

O objetivo é classificar conexões como `normal` ou `anomaly` usando apenas os arquivos oficiais. O `treino.csv` tem 69.833 registros e 49 atributos: 41 de tráfego do NSL-KDD, 5 derivados de outros atributos e 3 sinais operacionais (`score_ids_legado`, `tipo_alerta_soc` e `tempo_resposta_analista_min`). O `teste_sem_rotulo.csv` tem 24.333 registros. O treino tem 94,16% de conexões `normal` e 5,84% de `anomaly` (4.079 registros), uma razão de 16,1:1. Faltam 8,38% das células e só 321 linhas estão completas, então descartar linhas com ausentes não era uma opção. Escolhemos os modelos pelo **F1-macro**. Um classificador que sempre responde `normal` tem 94,16% de acurácia, mas F1-macro de 0,485, porque nunca detecta um ataque.

## 2. Qualidade dos dados, vazamento e protocolo

**Redundâncias e inconsistências.** Cinco colunas são funções exatas de outras (`src_bytes_kb`, `dst_bytes_kb`, `total_bytes`, `same_srv_pct` e `protocolo_cod`), e `num_outbound_cmds` é constante. Diferenças de caixa e espaços inflavam as categorias: depois da normalização, `protocol_type` passa de 6 para 3 categorias, `service` de 96 para 67 e `flag` de 19 para 11. Há 5.650 linhas com valores impossíveis, como taxas acima de 1 e bytes negativos. Também há 11.355 duplicatas exatas e **1.702 grupos de registros idênticos com classes opostas**. Esses grupos somam 3.730 linhas e 46,5% das anomalias, o que indica ruído de rótulo. Não há como saber qual dos dois rótulos é o correto.

**Vazamento.** Medimos a associação de todos os atributos com a classe: AUC e delta de Cliff para os numéricos, V de Cramér para os categóricos e informação mútua normalizada para todos. Os três sinais operacionais lideram o ranking (MI líquida de 0,546, 0,465 e 0,424). Em `tipo_alerta_soc = alerta`, 67,1% dos registros são anomalias, contra 1,1% em `ok`. O `tempo_resposta_analista_min` falta em 95,6% das normais e só em 23,5% das anomalias. Pelos nomes, essas informações surgem durante ou depois da triagem. Sem documentação sobre quando são geradas, **excluímos os três sinais por precaução**. Não afirmamos que houve vazamento, porque correlação sozinha não prova isso. Atributos de tráfego muito associados à classe, como `service` e `flag`, foram mantidos. A coluna `difficulty_level`, que seria vazamento pela própria origem, não existe nesta base.

**Protocolo.** Usamos `StratifiedGroupKFold` com 5 dobras e semente 42. Cada grupo reúne registros com atributos idênticos (56.766 grupos), então cópias nunca ficam em lados opostos. Com o KFold comum, 29,7% das linhas de validação teriam uma cópia no treino. Normalização, imputação, codificação, escala, filtro de conflitos, reamostragem, PCA e limiar foram ajustados dentro de um `Pipeline`, sempre só no treino de cada dobra. A validação nunca foi filtrada nem balanceada. Todas as etapas usaram as mesmas dobras (assinatura `8a814c72d149c698`). O teste nunca entrou em um ajuste: serviu apenas para conferir o esquema de colunas e para o `predict` final.

## 3. Pré-processamento: alternativas comparadas e decisões

Cada fator foi comparado com uma referência, um de cada vez, nas mesmas 5 dobras. A tabela mostra o F1-macro médio. A Árvore de Decisão serviu de modelo de referência, e o XGBoost foi usado como experimento complementar na etapa 2.

| Requisito | Alternativas comparadas | Resultado (F1-macro) | Decisão |
|---|---|---|---|
| Redundantes e inconsistentes | Conflitos: manter × remover só do treino | 0,8049 → **0,8717** (5/5 dobras) | Remover só do treino, sem trocar rótulos |
| | Duplicatas; derivadas e constante | −0,0232 (0/5); +0,0006 | Manter as duplicatas; remover as derivadas e a constante (−6 colunas) |
| | Categorias: brutas × normalizadas; fora do domínio: manter × ausente × recorte | −0,0021; +0,0003 / −0,0009 | Normalizar; tratar valores impossíveis como ausentes |
| | Ausentes: mediana ± indicador; `__ausente__` × moda | −0,0001; +0,0007 | Mediana e categoria `__ausente__` |
| Balanceamento | Nenhum × ROS 1:1 × RUS 1:1 × SMOTENC + Tomek (Árvore) | **0,8718** × 0,8668 × 0,7991 × 0,8633 | Não equilibrar as classes em 1:1 |
| | 27 configurações: razões de 0,05 a 1 e pesos de classe | XGBoost com peso √(n_normal/n_anomaly): 0,8744 contra 0,8702; Árvore com peso 2: 0,8721 contra 0,8713 | Preferir correções moderadas |
| Codificação (`service`) | One-Hot × One-Hot com categorias raras (< 100) agrupadas | 0,8706 → **0,8730** (5/5); 117 → 65–66 colunas | One-Hot com as raras agrupadas |
| Transformação numérica | Sem escala × Standard × Robust (Árvore); sem escala × Standard × `log1p` + Standard (MLP) | Árvore: 0,8706 / 0,8704 / 0,8706. MLP: 0,8225 / 0,8677 / **0,8701** | Sem escala nas árvores; `log1p` + Standard na MLP |
| Redução de dimensionalidade | Sem PCA × PCA com 25 × PCA com 50 componentes | **0,8704** × 0,8397 × 0,8537 (99,9% da variância) | Descartar o PCA |

Quase todo o ganho veio de remover os conflitos do treino. Com isso, o recall de `anomaly` da Árvore subiu de 0,55 para 0,77. Como a validação mantém os conflitos, o ganho não vem de uma avaliação mais fácil. O efeito colateral é que a prevalência de `anomaly` no treino cai de 5,84% para 3,30%, e o limiar 0,5 fica conservador demais. Equilibrar as classes em 1:1 corrigiu isso em excesso. O RUS descarta cerca de 97% das conexões normais e triplica os falsos positivos. O ROS só repete anomalias. Correções moderadas funcionaram melhor: peso de classe e, na etapa 3, ajuste do limiar de decisão. O agrupamento das categorias raras trata a cauda longa de `service`, em que 51 serviços somam 2% dos registros, e absorve as categorias que só aparecem no teste.

## 4. Classificadores e tabela comparativa

Comparamos três algoritmos:

- **Árvore de Decisão:** gini, sem limite de profundidade;
- **Random Forest:** 300 árvores, `max_features="sqrt"`;
- **MLP:** uma camada de 32 neurônios, ReLU, Adam, `max_iter=400` e `log1p` + Standard.

Cada algoritmo foi avaliado nas combinações P0 (referência sem tratamento), P1 (limpeza da seção 3), P2 (P1 com as categorias raras agrupadas), P3 (P2 com ROS 1:1) e P4 (P2 com RUS 1:1).

| Comb. | Balanc. | Algoritmo | F1-macro (média ± dp) | Precisão normal / anomaly | Recall normal / anomaly | FP / FN | Ajuste (s/dobra) |
|---|---|---|---|---|---|---|---|
| P0 | — | Árvore | 0,8050 ± 0,0056 | 0,973 / 0,734 | 0,988 / 0,552 | 816 / 1.828 | 1,09 |
| P0 | — | Random Forest | 0,8733 ± 0,0049 | 0,985 / 0,766 | 0,986 / 0,757 | 944 / 992 | 1,63 |
| P0 | — | MLP | 0,8570 ± 0,0080 | 0,982 / 0,749 | 0,985 / 0,713 | 976 / 1.170 | 8,97 |
| P1 | — | Árvore | 0,8706 ± 0,0044 | 0,986 / 0,741 | 0,983 / 0,774 | 1.105 / 924 | 0,60 |
| P1 | — | Random Forest | 0,8746 ± 0,0049 | 0,985 / 0,765 | 0,986 / 0,763 | 955 / 968 | 0,88 |
| P1 | — | MLP | 0,8722 ± 0,0041 | 0,986 / 0,752 | 0,984 / 0,767 | 1.031 / 950 | 4,36 |
| P2 | — | Árvore | 0,8730 ± 0,0038 | 0,986 / 0,743 | 0,983 / 0,780 | 1.099 / 897 | 0,41 |
| P2 | — | Random Forest | 0,8756 ± 0,0051 | 0,986 / 0,764 | 0,985 / 0,767 | 965 / 949 | 0,89 |
| P2 | — | MLP | 0,8701 ± 0,0044 | 0,985 / 0,750 | 0,984 / 0,762 | 1.037 / 973 | 3,78 |
| P3 | ROS 1:1 | Árvore | 0,8630 ± 0,0045 | 0,984 / 0,736 | 0,983 / 0,749 | 1.098 / 1.024 | 0,40 |
| P3 | ROS 1:1 | Random Forest | 0,8779 ± 0,0036 | 0,986 / 0,764 | 0,985 / 0,776 | 978 / 912 | 1,22 |
| P3 | ROS 1:1 | MLP | 0,8686 ± 0,0028 | 0,986 / 0,732 | 0,982 / 0,776 | 1.162 / 914 | 5,87 |
| P4 | RUS 1:1 | Árvore | 0,7973 ± 0,0092 | 0,988 / 0,508 | 0,951 / 0,814 | 3.223 / 758 | 0,14 |
| P4 | RUS 1:1 | Random Forest | 0,8516 ± 0,0048 | 0,988 / 0,649 | 0,973 / 0,815 | 1.797 / 754 | 0,31 |
| P4 | RUS 1:1 | MLP | 0,8289 ± 0,0044 | 0,988 / 0,589 | 0,965 / 0,810 | 2.309 / 777 | 0,69 |
| P2 | — | Árvore (aninhada) | 0,8725 ± 0,0043 | 0,986 / 0,743 | 0,983 / 0,779 | 1.099 / 903 | 0,42 |
| P2 | — | MLP (aninhada) | 0,8725 ± 0,0038 | 0,986 / 0,753 | 0,984 / 0,768 | 1.028 / 948 | 4,45 |
| P2 | pesos moderados | RF (aninhada) | 0,8800 ± 0,0022 | 0,987 / 0,763 | 0,985 / 0,786 | 998 / 872 | 1,73 |
| P2 | pesos moderados | **RF (aninhada + limiar)** | **0,8818 ± 0,0007** | 0,988 / 0,756 | 0,984 / 0,801 | 1.055 / 812 | 1,73 |

*FP e FN somados nas 5 dobras. Nas variantes "aninhadas", os hiperparâmetros e, quando indicado, o limiar são escolhidos em 3 dobras internas por grupo, dentro de cada treino externo. O tempo é de relógio, e a RF usa todos os núcleos.*

A **Random Forest liderou em todas as combinações** e venceu 24 das 25 comparações pareadas por dobra. A média de 300 árvores atenua o ruído, por isso a limpeza ajudou bem mais a Árvore (+0,0656) e a MLP (+0,0152) do que a RF (+0,0013). Em `normal`, o F1 fica em torno de 0,985 em quase todos os casos, então a diferença entre os modelos aparece na classe `anomaly`. O RUS piorou os três algoritmos, que chegaram a ter de 1.797 a 3.223 falsos positivos. Na RF aninhada, a seleção interna escolheu pesos moderados (`{0: 1, 1: 4}` ou `{0: 1, 1: 2}`), `max_features=0,3` e limiares entre 0,34 e 0,45.

O vencedor foi escolhido por uma regra fixada antes da comparação: maior F1-macro; em empate (diferença < 0,0005), maior F1 de `anomaly`; depois, mais vitórias pareadas; por fim, menor desvio. A **RF aninhada com limiar (P2)** venceu já no primeiro critério. Ela superou 19 dos outros 20 candidatos em todas as dobras, e a RF aninhada sem ajuste de limiar em 4 das 5. Numa segunda divisão por grupos (semente 137), manteve 0,8818 ± 0,0037, contra 0,8706 da Árvore e 0,8710 da MLP. Pela correção de Tibshirani e Tibshirani (2009), o otimismo da seleção é de cerca de 0,0001.

## 5. Modelo final, desempenho esperado e submissão

O modelo final é uma `RandomForestClassifier` com 300 árvores, `max_features=0,3`, `min_samples_leaf=1`, `class_weight={0: 1, 1: 4}` e `random_state=42`, sobre o pré-processamento P2. Ela classifica como `anomaly` quando P(`anomaly`) ≥ 0,37. O modelo foi ajustado uma única vez sobre todo o `treino.csv`, e o filtro de conflitos atuou só nesse ajuste, deixando 66.103 das 69.833 linhas.

Na etapa 4, refizemos a seleção interna, que escolheu os mesmos hiperparâmetros. O melhor limiar neste ambiente foi 0,39, com F1 interno de 0,8803 contra 0,8800 em 0,37. Mantivemos 0,37: trocar de limiar agora seria uma nova seleção feita depois de escolhido o vencedor. Dois ajustes independentes geram árvores idênticas. A inferência roda em uma única thread, porque a soma paralela das probabilidades pode inverter registros que caem exatamente no limiar (111/300 = 0,37).

**Desempenho esperado.** Os valores abaixo vêm da validação aninhada fora da dobra, com 69.833 previsões do treino. Não são métricas do teste.

| Classe | Precisão | Recall | F1 | Suporte |
|---|---|---|---|---|
| `normal` | 0,9876 | 0,9840 | 0,9858 | 65.754 |
| `anomaly` | 0,7559 | 0,8009 | 0,7778 | 4.079 |
| **F1-macro** | | | **0,8818** (IC 95%: 0,8794–0,8843) | 69.833 |

A matriz agregada tem TN = 64.699, FP = 1.055, FN = 812 e TP = 3.267. Dos 1.867 erros, **1.710 (91,6%) estão nos grupos conflitantes**, onde qualquer classificador determinístico erra pelo menos um registro por grupo. Mesmo um oráculo ficaria entre 0,869 e 0,905. Nas 66.103 linhas sem conflito, o modelo erra 157 vezes, com F1-macro de 0,9814. Por isso, o F1-macro oficial deve ficar perto de 0,88 se o teste tiver o mesmo ruído, e mais alto se tiver menos conflitos. A avaliação no próprio treino daria 0,8921, um valor inflado que não usamos.

**Arquivo enviado.** O `submissao_10.csv` tem cabeçalho `id,class_prevista` e 24.333 linhas, na ordem do teste. Prevê 23.125 conexões `normal` (95,04%) e 1.208 `anomaly` (4,96%). Essa proporção só descreve as previsões e não mede acerto. O arquivo passou em todas as conferências de formato e reprodução. Um modelo treinado do zero gera o mesmo arquivo, byte a byte. O sha256 está na ficha da entrega (notebook 04, seção 5.2). As métricas oficiais e o ranking serão incluídos quando forem divulgados.

## 6. Explicabilidade

Usamos **SHAP** (`TreeExplainer`, intervencional, saída em probabilidade) sobre a P(`anomaly`) da floresta final. Foram 200 registros do treino filtrado, com outros 100 como referência. O modelo não foi alterado e o teste não foi usado. As maiores contribuições médias absolutas foram de `dst_bytes` (0,0121), `service = private` (0,0060), `dst_host_rerror_rate` (0,0049) e `src_bytes` (0,0048). O serviço `private`, o protocolo `icmp` e taxas de erro altas aumentam a P(`anomaly`), o que é coerente com varreduras de portas e negação de serviço. A importância por impureza (MDI) da etapa 3, calculada em todo o treino, também destaca as taxas de erro SYN e a concentração de serviços. Os maiores valores são de `dst_host_srv_serror_rate` (0,107), `same_srv_rate` (0,087), `srv_serror_rate` (0,075) e `count` (0,057).

As duas visões diferem por três motivos:

- a amostra do SHAP tem 197 conexões normais e só 3 anomalias;
- o MDI favorece atributos contínuos;
- atributos correlacionados dividem a importância entre si.

Essas medidas mostram associações aprendidas pelo modelo, e não causas de ataques.

## 7. Limitações

- A exclusão dos sinais operacionais é preventiva e depende de confirmação da professora. Se o vazamento for confirmado, a exclusão continua mesmo que eles aumentem o F1.
- As decisões das etapas 2 e 3 usaram as mesmas dobras, e a divisão 137 reutiliza os mesmos registros. A correção de otimismo cobre só a escolha final entre 21 candidatos.
- O filtro de conflitos não decide qual rótulo é o correto. No teste, esses casos continuam como erros inevitáveis.
- O limiar foi calibrado com modelos de cerca de 44 mil linhas, e o modelo final usa 66 mil. Versões diferentes das bibliotecas mudam o F1 interno em cerca de 0,0002.
- As dobras agrupam só cópias exatas. Conexões quase idênticas podem ter ficado em lados opostos.

## 8. Contribuições e uso de IA

| Integrante | Etapa 1 | Etapa 2 | Etapa 3 | Etapa 4 |
|---|---|---|---|---|
| Samuel Lucas Rodrigues Vieira | Estrutura, tipos e ausentes | Ausentes, redundâncias e dobras por grupo | Árvore e protocolo comum | Treino final |
| Matheus de Almeida Moreira | Desbalanceamento | Balanceamento | Random Forest | Diagnóstico da validação |
| Arthur Soares Rolla | Categorias | Codificação e escala | MLP | Explicabilidade |
| Carlos Eduardo de Melo Sabino | Redundâncias e outliers | PCA | Tabela comparativa | CSV de submissão |
| Paulo Gabriel de Oliveira Leite | Associação e vazamento | Integração | Seleção e auditoria | Relatório e conferência |

**Uso de IA generativa.** Usamos três ferramentas:

- **OpenAI Codex:** organização dos roteiros, implementação de experimentos e revisão de textos nas etapas 1 a 3.
- **Claude Code (Anthropic):** implementação e revisão nas etapas 3 e 4, incluindo o treino final, a conferência da entrega e a redação deste relatório a partir das saídas dos notebooks.
- **Gemini, via Antigravity:** implementação e revisão na etapa 3 e no diagnóstico de validação da etapa 4.

Os números citados vêm das saídas executadas dos notebooks. A responsabilidade pelas decisões e interpretações é da equipe.
