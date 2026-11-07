# Detecção de intrusão em redes — roteiro da equipe

**Professora:** Cristiane Neri Nobre. **Equipe:** Grupo 10.

**Integrantes:**

- Arthur Soares Rolla
- Carlos Eduardo de Melo Sabino
- Matheus de Almeida Moreira
- Paulo Gabriel de Oliveira Leite
- Samuel Lucas Rodrigues Vieira

A primeira entrega está em `notebooks/01_analise_exploratoria.ipynb`: análise exploratória do treino oficial, cinco sínteses e diagnóstico consolidado. O notebook inclui a declaração de uso do OpenAI Codex como apoio à organização, revisão, correção e verificação da execução. O notebook 02 tem as partes 1–4 implementadas; sua parte 5 e os notebooks 03–04 continuam como roteiros.

A parte 2 do notebook 02 compara ausência de balanceamento, RandomOverSampler, RandomUnderSampler e SMOTENC seguido de Tomek Links, com Árvore de Decisão e XGBoost nas mesmas cinco dobras por grupos. SMOTENC adapta a proposta SMOTETomek aos atributos categóricos da base. Instale `requirements.txt` e execute o notebook em ordem, a partir da raiz ou de `notebooks/`; a parte 2 reutiliza a carga, as dobras e a configuração da parte 1. XGBoost é um experimento adicional, sujeito à confirmação de que atende à exigência de algoritmo visto em aula para a etapa 3.

As seções 2.4–2.6 ampliam a comparação para 27 configurações por modelo, incluindo cinco proporções de reamostragem, SMOTENC sem Tomek, Tomek isolado e pesos de classe. Foram executados 300 ajustes adicionais, com verificação dos finalistas em outra divisão por grupos. A proposta exploratória atual é XGBoost com `scale_pos_weight = sqrt(n_normal / n_anomaly)`, calculado apenas no treino filtrado de cada dobra: F1-macro médio 0,8744, contra 0,8702 sem balanceamento nas duas divisões. As duas divisões reutilizam os mesmos registros e não constituem um teste independente; a conclusão e as limitações estão na seção 2.6.

A origem e a disponibilidade temporal dos três sinais operacionais ainda precisam ser confirmadas com a professora. O notebook documenta essa limitação e recomenda exclusão preventiva. Não apresenta a suspeita como vazamento comprovado.

## Entrega 1 — 01/11/2026

- Entregar o notebook `notebooks/01_analise_exploratoria.ipynb`, com as saídas salvas.
- Para reproduzir, instalar as dependências de `requirements.txt`, manter `data/treino.csv` e executar **Restart & Run All** a partir da raiz ou de `notebooks/`.
- O diagnóstico consolidado está no próprio notebook. Relatório final, modelos e CSV de previsões pertencem às etapas seguintes.
- A identificação da equipe foi fornecida para esta entrega. As seções do notebook são temáticas e não atribuem contribuições individuais não confirmadas.

## Base oficial

- `data/treino.csv`: treino com alvo `class` (`normal` ou `anomaly`).
- `data/teste_sem_rotulo.csv`: teste sem classe, com `id`.
- `data/modelo_de_submissao.csv`: formato exigido (`id`, `class_prevista`).

Não usar os arquivos NSL-KDD antigos, não remapear para cinco famílias e não criar outra separação oficial. A validação interna é permitida apenas dentro do treino. O teste não oferece gabarito: as métricas oficiais serão calculadas pela professora.

## Uma tarefa para cada membro em cada notebook

A tabela abaixo preserva a distribuição de trabalho por posições de integrante, sem presumir o vínculo entre cada posição e os nomes. O notebook 01 apresenta as análises concluídas por seção temática. Nos notebooks 02–04, as seções descrevem tarefa, entregável, célula TODO e espaço para resultados e justificativa.

| Integrante | 01 — Análise exploratória | 02 — Pré-processamento | 03 — Classificadores | 04 — Entrega final |
|---|---|---|---|---|
| Membro 1 | Carga, estrutura, tipos e ausentes | Ausentes, redundâncias e inconsistências | Árvore de Decisão e protocolo comum | Reconstrução e treino final |
| Membro 2 | Classes e desbalanceamento | Duas técnicas de balanceamento | Random Forest | Diagnóstico das métricas de validação |
| Membro 3 | Categorias e cardinalidade | Codificação e transformação numérica | MLP ou terceiro algoritmo visto em aula | Explicabilidade do vencedor |
| Membro 4 | Redundâncias, inconsistências e outliers | Redução de dimensionalidade ou seleção de instâncias | Tabela comparativa estruturada | Previsões e CSV de submissão |
| Membro 5 | Associação de todos os atributos, leakage e diagnóstico | Integração e comparação das estratégias | Seleção e auditoria metodológica | Relatório, apresentação e conferência da entrega |

Todos participam da revisão e precisam compreender o fluxo completo. O responsável pela integração depende dos resultados dos demais. Não deve executar sozinho as tarefas individuais.

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
- Usar validação interna por grupos de registros equivalentes, buscando estratificação das classes. Manter cópias no mesmo grupo e usar as mesmas dobras nas comparações.
- Ajustar imputação, codificação, normalização, balanceamento e redução apenas no treino de cada dobra.
- Comparar explicitamente estratégias para dados redundantes/inconsistentes, pelo menos dois balanceamentos, codificação, transformação numérica e redução de dimensionalidade **ou seleção de instâncias**.
- Comparar pelo menos três classificadores vistos em aula. Selecionar pelo F1-macro de validação interna e explicar o vencedor.
- Gerar `submissao_<número_da_equipe>.csv` sem alterar IDs ou ordem, com classes apenas `normal`/`anomaly`, sem vazios, ausências, repetições ou IDs extras.
- O notebook entregue deve reproduzir exatamente o CSV enviado. Informar o número real do grupo.
- Declarar uso de IA e contribuições efetivas dos integrantes.

## Arquivos de apoio

`src/` contém estrutura legada, com referências à base antiga e funções incompletas. O notebook 01 lê `treino.csv` diretamente e não depende desses módulos. Sua adaptação pertence às próximas etapas.

As 49 células de código do notebook 01 foram executadas em ordem em uma sessão nova de kernel Python, sem erros, e as saídas foram atualizadas. O ambiente é registrado na célula de importação. As cinco sínteses foram revisadas para distinguir resultados descritivos, hipóteses de vazamento e propostas para a próxima etapa.

`reports/estrutura_relatorio.md` permanece como roteiro do relatório final. Não há modelos finais ou arquivo de submissão nesta entrega exploratória.
