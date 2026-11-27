# Roteiro da apresentação final — Grupo 10

Duração prevista de cerca de 10 minutos, em 10 slides (ajustar ao tempo definido pela professora). Cada integrante apresenta a parte que fez. Os números vêm de [relatorio_final.md](relatorio_final.md), e os gráficos, dos notebooks. A coluna "Fonte" indica a célula de onde exportar cada figura.

| # | Slide | Mensagem principal | Conteúdo | Fonte | Quem | Tempo |
|---|---|---|---|---|---|---|
| 1 | Problema e métrica | Acurácia engana quando 94% das conexões são normais | 69.833 registros no treino, 5,84% de `anomaly`. O classificador "sempre normal" tem 94,16% de acurácia, mas F1-macro de 0,485 | Notebook 01, seção 2 | Matheus | 0:45 |
| 2 | O que encontramos nos dados | Há ruído de rótulo e sinais suspeitos | 1.702 grupos de registros idênticos com classes opostas (46,5% das anomalias), 5 colunas derivadas, 1 constante, categorias com grafias diferentes e 5.650 linhas fora do domínio | Notebook 01, seções 1 e 4 | Samuel / Carlos Eduardo | 1:00 |
| 3 | Vazamento | Os três sinais operacionais ficaram de fora por precaução | Ranking de MI com os três no topo. `tempo_resposta_analista_min` falta em 95,6% das normais. Correlação não prova vazamento: a decisão se baseia na origem e no momento em que a informação existe | Notebook 01, seção 5.6 | Paulo | 1:00 |
| 4 | Protocolo sem vazamento | Tudo é ajustado dentro da dobra, e as cópias não se dividem | `StratifiedGroupKFold` por registro idêntico. Com o KFold comum, 29,7% das linhas de validação teriam uma cópia no treino. A validação nunca é filtrada nem balanceada | Notebook 02, seção 1.4 | Samuel | 0:45 |
| 5 | Pré-processamento comparado | O maior ganho veio de tirar os conflitos do treino | Tabela da seção 3 do relatório: conflitos +0,067, raras agrupadas +0,002, escalas neutras para árvores, PCA pior (−0,017 a −0,031), balanceamento 1:1 pior | Notebook 02, seções 1.5, 2.6, 3.5, 4 e 5.5 | Arthur / Carlos Eduardo | 1:30 |
| 6 | Três algoritmos | A Random Forest lidera em todas as combinações | Gráfico de F1-macro (média ± dp) por combinação e algoritmo. RUS derruba todos os modelos (até 3.223 falsos positivos) | Notebook 03, seção 4.2 | Arthur / Matheus | 1:00 |
| 7 | Vencedor e por quê | Pesos moderados e limiar corrigem a prevalência baixa | RF aninhada com limiar 0,37: 0,8818 ± 0,0007. Supera 19 dos outros 20 candidatos em 5/5 dobras e mantém 0,8818 na divisão 137 | Notebook 03, seções 5.3 e 5.4 | Paulo | 1:00 |
| 8 | Desempenho esperado | 92% dos erros estão nos conflitos, que nenhum modelo resolve | Métricas por classe e matriz de confusão fora da dobra. Nas linhas sem conflito, o F1-macro é 0,98. Separar métricas internas das oficiais | Notebook 04, seções 2.1 e 2.2 | Matheus | 1:00 |
| 9 | Explicabilidade | O modelo usa taxas de erro, serviço e volume de bytes | Gráficos de barras e beeswarm do SHAP, comparados com a importância MDI. Associação não é causa | Notebook 04, seção 3.3 | Arthur | 1:00 |
| 10 | Entrega e reprodução | O CSV é reproduzido byte a byte | `submissao_10.csv`: 24.333 linhas, 4,96% previstas como `anomaly`, checklist completo e sha256. Limitações e uso de IA | Notebook 04, seções 4 e 5 | Carlos Eduardo / Paulo | 1:00 |

## Mensagens para a fala final (30 s)

- A escolha foi feita só com validação interna. O teste não participou de nenhum ajuste.
- O F1-macro oficial deve ficar perto de 0,88 se o teste tiver o mesmo ruído do treino.
- O ranking e as métricas oficiais serão incluídos quando a professora divulgar o resultado.

## Perguntas prováveis e respostas curtas

- **Por que excluir sinais tão preditivos?** Porque não sabemos quando essa informação é gerada. Se ela vier depois da triagem do analista, usá-la seria vazamento. Um ganho de F1 não prova que o uso é legítimo.
- **Remover conflitos não é trapaça?** Não. A remoção vale só para o treino de cada dobra, e a validação continua com todos os registros, inclusive os conflitantes.
- **Por que limiar de 0,37 e não 0,5?** O filtro reduz a prevalência de anomalias no treino de 5,84% para 3,30%. O limiar foi escolhido nas dobras internas, sem usar a validação externa nem o teste.
- **Por que não SMOTE?** SMOTENC + Tomek foi testado na etapa 2. Piorou o F1-macro (0,8633 contra 0,8718) e custou de 20 a 30 vezes mais tempo.
- **Por que o PCA foi descartado?** Mesmo mantendo 99,9% da variância, reduziu o F1 de `anomaly` (de 0,756 para 0,725).
