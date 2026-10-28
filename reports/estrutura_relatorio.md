# Roteiro do relatório final — 3 a 5 páginas

**Equipe:** preencher número e nomes do grupo do CANVAS.
**Professora:** Cristiane Neri Nobre.

Este documento distribui a redação; não contém resultados nem decisões já tomadas. Preencher após o trabalho autoral nos notebooks.

## 1. Problema e diagnóstico — membros 1 e 2

Apresentar os CSVs oficiais, alvo binário, dimensões, tipos, ausências, proporção das classes e motivo para usar F1-macro. Usar números calculados na nova base, sem reutilizar os resultados da versão antiga.

## 2. Qualidade dos dados e vazamento — membros 4 e 5

Apresentar evidências de redundâncias e inconsistências, análise de associação de todos os atributos com a classe e justificativa das exclusões decididas pela equipe. Examinar a disponibilidade temporal dos sinais operacionais adicionados; correlação isolada não prova leakage.

Descrever o protocolo de validação apenas dentro do treino, controle de duplicatas entre dobras e isolamento do teste oficial.

## 3. Pré-processamento — contribuições dos cinco membros

Justificar tratamento de ausentes/redundâncias/inconsistências, dois balanceamentos, codificação e cardinalidade de service, transformação numérica e redução de dimensionalidade ou seleção de instâncias. Descrever comparações explícitas com uma referência, sempre com ajuste dentro das dobras.

## 4. Modelos e tabela comparativa — membros 1–4; seleção pelo membro 5

Descrever pelo menos três algoritmos vistos em aula, parâmetros, sementes e resultados reais. Consolidar:

| Estratégia de pré-processamento | Balanceamento | Algoritmo | F1-macro médio ± desvio | Precisão por classe | Recall por classe | Tempo |
|---|---|---|---|---|---|---|
| A preencher após execução | | | | | | |

Discutir ganhos, perdas e limitações; justificar o vencedor sem usar o teste.

## 5. Explicabilidade, reprodução e entrega — membros 1–5

Membro 3: interpretar a explicabilidade do vencedor. Membro 2: distinguir métricas internas das oficiais.
Membros 1 e 4: explicar reconstrução do pipeline, treino final, geração e validação do CSV e reprodução do arquivo enviado.
Membro 5: consolidar limitações, contribuições, declaração de IA e revisão final.

O teste não tem rótulos: incluir métricas oficiais e ranking somente após divulgação da professora.
Declarar ferramenta de IA e finalidade efetivamente utilizadas, inclusive apoio do OpenAI Codex à organização dos roteiros; não alegar revisões ainda não realizadas.
