# Detecção de intrusão em redes — roteiro da equipe

**Professora:** Cristiane Neri Nobre. **Equipe:** Grupo 10.

**Integrantes:**

- Arthur Soares Rolla
- Carlos Eduardo de Melo Sabino
- Matheus de Almeida Moreira
- Paulo Gabriel de Oliveira Leite
- Samuel Lucas Rodrigues Vieira

A primeira entrega está em `notebooks/01_analise_exploratoria.ipynb`: análise exploratória do treino oficial, cinco sínteses e diagnóstico consolidado. O notebook 02 (`notebooks/02_pre_processamento.ipynb`) implementa e compara as partes 1–5 de pré-processamento e balanceamento. O notebook 03 (`notebooks/03_classificadores.ipynb`) implementa e compara os três algoritmos obrigatórios da Etapa 3 (Árvore de Decisão, Random Forest e MLP) nas cinco dobras por grupos (`ASSINATURA_DOBRAS = 8a814c72d149c698`), com seleção aninhada de hiperparâmetros e auditoria metodológica. O notebook 04 (`notebooks/04_avaliacao_final.ipynb`) consolida o pipeline final em todo `treino.csv`, o diagnóstico fora da dobra, a explicabilidade (SHAP e permutação OOF), a geração determinística de `submissao_10.csv` e a auditoria final da entrega, acompanhado por `reports/relatorio_final.md` e `reports/roteiro_apresentacao.md`.

A parte 2 do notebook 02 compara ausência de balanceamento, RandomOverSampler, RandomUnderSampler e SMOTENC seguido de Tomek Links, com Árvore de Decisão e XGBoost nas mesmas cinco dobras por grupos. SMOTENC adapta a proposta SMOTETomek aos atributos categóricos da base. Instale `requirements.txt` e execute o notebook em ordem, a partir da raiz ou de `notebooks/`; a parte 2 reutiliza a carga, as dobras e a configuração da parte 1. XGBoost é um experimento adicional, sujeito à confirmação de que atende à exigência de algoritmo visto em aula para a etapa 3.

As seções 2.4–2.6 ampliam a comparação para 27 configurações por modelo, incluindo cinco proporções de reamostragem, SMOTENC sem Tomek, Tomek isolado e pesos de classe. Foram executados 300 ajustes adicionais, com verificação dos finalistas em outra divisão por grupos. A proposta exploratória atual é XGBoost com `scale_pos_weight = sqrt(n_normal / n_anomaly)`, calculado apenas no treino filtrado de cada dobra: F1-macro médio 0,8744, contra 0,8702 sem balanceamento nas duas divisões. As duas divisões reutilizam os mesmos registros e não constituem um teste independente; a conclusão e as limitações estão na seção 2.6.

A origem e a disponibilidade temporal dos três sinais operacionais ainda precisam ser confirmadas com a professora. O notebook documenta essa limitação e recomenda exclusão preventiva. Não apresenta a suspeita como vazamento comprovado.

A parte 5 integra limpeza, codificação, balanceamento e PCA em dez estratégias, comparadas com Árvore de Decisão e XGBoost nas mesmas cinco dobras por grupos. Os dois melhores candidatos de cada modelo são reavaliados com a referência M1 na divisão de semente 137. As tabelas distinguem comparações controladas de combinações de fatores e registram métricas por classe, dimensões, tempos e contagens. `CONFIGS_ETAPA3_M5` contém as propostas exploratórias e `ajustar_configuracao_m5` reconstrói o pipeline, incluindo o filtro de conflitos restrito ao treino recebido. A integração mantém os sinais operacionais excluídos e não consulta o teste oficial.

Na Etapa 3 (`notebooks/03_classificadores.ipynb`), Árvore de Decisão, Random Forest e MLP (`log1p + StandardScaler`) são avaliados sobre P0–P4 e por validação aninhada em P2 (21 candidatos x 5 dobras, executados do início ao fim em kernel limpo do `.venv` sem avisos ou erros). Pelo critério determinístico de seleção (independente de tempo de máquina), vence `Random Forest (aninhada + limiar)` em P2 (`F1-macro = 0,8818 ± 0,0007` na divisão 42 e `0,8818 ± 0,0037` na divisão 137; `class_weight={0: 1.0, 1: 4.0}`, `max_features=0.3`, `limiar_decisao=0.37`), com configuração e funções reprodutíveis registradas em `CONFIG_VENCEDOR_ETAPA3`, `construir_pipeline_vencedor` e `prever_vencedor`.

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

## Divisão de tarefas e contribuições nos notebooks

Os notebooks 01 a 04 estão concluídos, executados e revisados pelo Grupo 10, com código, saídas e justificativas em cada seção:

| Integrante | 01 — Análise exploratória | 02 — Pré-processamento | 03 — Classificadores | 04 — Entrega final |
|---|---|---|---|---|
| Samuel Lucas Rodrigues Vieira | Estrutura, tipos e ausentes | Ausentes, redundâncias e dobras por grupo | Árvore de Decisão e protocolo comum | Reconstrução e treino final |
| Matheus de Almeida Moreira | Classes e desbalanceamento | Técnicas de balanceamento | Random Forest | Diagnóstico das métricas de validação |
| Arthur Soares Rolla | Categorias e cardinalidade | Codificação e transformação numérica | MLP | Explicabilidade do vencedor |
| Carlos Eduardo de Melo Sabino | Redundâncias, inconsistências e outliers | PCA | Tabela comparativa estruturada | Previsões e CSV de submissão |
| Paulo Gabriel de Oliveira Leite | Associação, leakage e diagnóstico | Integração e comparação | Seleção e auditoria metodológica | Relatório, apresentação e conferência |

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

## Entregáveis consolidados

- **Notebooks autocontidos (Etapas 1 a 4):** `notebooks/01_analise_exploratoria.ipynb`, `notebooks/02_pre_processamento.ipynb`, `notebooks/03_classificadores.ipynb` e `notebooks/04_avaliacao_final.ipynb` (todos executados em ordem, sem erros e sem dependência de módulos externos).
- **Artefatos do modelo e submissão:** `models/config_final.json` (impressão digital `676b7dadfe54344b`, limiar `0,37`) e `submissao_10.csv` (`24.333` previsões reproduzíveis byte a byte).
- **Relatórios e apresentação:** `reports/relatorio_final.md`, `reports/relatorio_final_sbc/relatorio_final.pdf` (template SBC) e `reports/roteiro_apresentacao.md`.
