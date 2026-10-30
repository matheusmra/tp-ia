# Detecção de intrusão em redes — roteiro da equipe

Professora: Cristiane Neri Nobre. Este projeto organiza as tarefas dos cinco integrantes conforme os novos CSVs e o enunciado. **O notebook 01 reaproveita o código anterior dos membros 1–4, adaptado à nova base. Os notebooks 02–04 continuam como roteiros, sem implementação.** Cada membro deve revisar, completar e justificar sua seção. A seção do Membro 5 do notebook 01 (associação de todos os atributos, investigação de vazamento, auditoria de conformidade e diagnóstico consolidado) está implementada; permanece pendente apenas a confirmação, com a professora, da origem dos três sinais operacionais.

## Base oficial

- `data/treino.csv`: treino com alvo `class` (`normal` ou `anomaly`).
- `data/teste_sem_rotulo.csv`: teste sem classe, com `id`.
- `data/modelo_de_submissao.csv`: formato exigido (`id`, `class_prevista`).

Não usar os arquivos NSL-KDD antigos, não remapear para cinco famílias e não criar outra separação oficial. A validação interna é permitida apenas dentro do treino. O teste não oferece gabarito: as métricas oficiais serão calculadas pela professora.

## Uma tarefa para cada membro em cada notebook

Substituir os identificadores pelos nomes do grupo do CANVAS. No notebook 01, cada seção preserva o código reaproveitável e indica a revisão ou complemento necessário. Nos notebooks 02–04, as seções descrevem tarefa, entregável, célula TODO e espaço para resultados e justificativa.

| Integrante | 01 — Análise exploratória | 02 — Pré-processamento | 03 — Classificadores | 04 — Entrega final |
|---|---|---|---|---|
| Membro 1 | Carga, estrutura, tipos e ausentes | Ausentes, redundâncias e inconsistências | Árvore de Decisão e protocolo comum | Reconstrução e treino final |
| Membro 2 | Classes e desbalanceamento | Duas técnicas de balanceamento | Random Forest | Diagnóstico das métricas de validação |
| Membro 3 | Categorias e cardinalidade | Codificação e transformação numérica | MLP ou terceiro algoritmo visto em aula | Explicabilidade do vencedor |
| Membro 4 | Redundâncias, inconsistências e outliers | Redução de dimensionalidade ou seleção de instâncias | Tabela comparativa estruturada | Previsões e CSV de submissão |
| Membro 5 | Associação de todos os atributos, leakage e diagnóstico | Integração e comparação das estratégias | Seleção e auditoria metodológica | Relatório, apresentação e conferência da entrega |

Todos participam da revisão e precisam compreender o fluxo completo. O responsável pela integração depende dos resultados dos demais; não deve executar sozinho as tarefas individuais.

## Cronograma de 2026

| Etapa | Prazo | Valor | Entrega |
|---|---|---|---|
| 1 | 01/11 | 2,00 | Notebook de análise exploratória e diagnóstico |
| 2 | 07/11 | 4,00 | Notebook de experimentos de pré-processamento |
| 3 | 21/11 | 4,00 | Notebook com três classificadores e tabela comparativa |
| 4 | 28/11 | 5,00 | Notebook completo, relatório de 3–5 páginas, CSV e apresentação |

## Regras para a implementação pela equipe

- Investigar a associação de cada atributo com a classe antes do treinamento e justificar possíveis exclusões. Correlação não comprova vazamento por si só.
- Investigar a origem e disponibilidade dos sinais adicionados, incluindo `score_ids_legado`, `tipo_alerta_soc` e `tempo_resposta_analista_min`.
- Ajustar imputação, codificação, normalização, balanceamento e redução apenas no treino de cada dobra.
- Comparar explicitamente estratégias para dados redundantes/inconsistentes, pelo menos dois balanceamentos, codificação, transformação numérica e redução de dimensionalidade **ou seleção de instâncias**.
- Comparar pelo menos três classificadores vistos em aula. Selecionar pelo F1-macro de validação interna e explicar o vencedor.
- Gerar `submissao_<número_da_equipe>.csv` sem alterar IDs ou ordem, com classes apenas `normal`/`anomaly`, sem vazios, ausências, repetições ou IDs extras.
- O notebook entregue deve reproduzir exatamente o CSV enviado. Informar o número real do grupo.
- Declarar uso de IA e contribuições efetivas dos integrantes.

## Arquivos de apoio

`src/` e `requirements.txt` foram devolvidos à versão anterior à implementação indevida. São estrutura **legada**, ainda com referências à base antiga e funções incompletas; a adaptação desses módulos faz parte das tarefas dos membros. O notebook 01 lê treino.csv diretamente, sem depender desses módulos; os demais roteiros não os executam.

A versão antiga registrada no histórico Git foi a base do reaproveitamento no notebook 01. Suas conclusões numéricas e saídas foram retiradas para não confundi-las com a nova base. As células de código existentes foram verificadas com treino.csv e as cinco sínteses do notebook 01 estão preenchidas. O notebook 01 foi validado com Restart & Run All: 49 células de código executam em ordem, sem erros e sem dependência de estado oculto.

`reports/estrutura_relatorio.md` contém o roteiro do relatório a ser escrito pela equipe. Não há resultados de modelos ou arquivo de submissão final entregues nesta adaptação.
