# Relatório final — Análise de Recursos Humanos

## Objetivo e método

Este relatório responde às questões do projeto prático de People Analytics usando a base `funcionarios_historico.csv`. A base possui registros periódicos dos mesmos colaboradores; portanto, cada linha não representa uma pessoa diferente. Para o quadro atual, foi usado o snapshot mais recente (**31/12/2023**) e, para análises históricas, foram preservados os snapshots. As médias salariais usam apenas salários positivos.

## 1. Exploração inicial

A base contém **50,000 registros** e **10,155 funcionários únicos**, distribuídos em 19 colunas. Os tipos reconhecidos na leitura estão listados abaixo.

| Coluna | Tipo lido |
| --- | --- |
| id_registro | int64 |
| id_funcionario | int64 |
| nome_funcionario | str |
| idade | int64 |
| sexo | str |
| escolaridade | str |
| departamento | str |
| cargo | str |
| nivel_hierarquico | int64 |
| salario | str |
| data_admissao | str |
| data_desligamento | str |
| data_referencia | str |
| tipo_contrato | str |
| modalidade_trabalho | str |
| avaliacao_desempenho | float64 |
| horas_treinamento | int64 |
| quantidade_promocoes | int64 |
| status_funcionario | str |

Problemas observados: campos ausentes em escolaridade e departamento; a ausência de data de desligamento é esperada para muitos registros ativos; também foram identificadas idades fora da faixa plausível e valores salariais negativos. O mesmo funcionário aparecer em várias linhas é característica do painel, não duplicidade por si só.

## 2. Limpeza e qualidade dos dados

- Removidos **0** registros totalmente duplicados ou com `id_registro` repetido. Os IDs de funcionários repetidos foram mantidos porque representam snapshots diferentes.
- **158** valores de idade fora da faixa de 18 a 100 foram tratados como ausentes. Foram preenchidos pela mediana válida do próprio funcionário e, quando indisponível, pela mediana geral.
- **86** salários nulos ou não positivos foram excluídos dos cálculos salariais, sem inventar valores.
- Datas foram convertidas para data; **150** datas de admissão que não puderam ser interpretadas foram excluídas apenas das análises que dependem dessa data.
- Campos ausentes de departamento e escolaridade foram identificados como “Não informado”. As datas de desligamento vazias foram preservadas, pois normalmente indicam vínculo ativo.

| Coluna | Valores ausentes |
| --- | --- |
| escolaridade | 150 |
| departamento | 150 |
| data_desligamento | 46009 |

## 3. Distribuição do quadro corporativo

No último snapshot há **6,710 colaboradores**, dos quais **6,163 estão ativos**. A tabela considera somente ativos e conta cada funcionário uma vez.

| Departamento | Funcionários |
| --- | --- |
| Tecnologia | 1060 |
| Recursos Humanos | 1043 |
| Marketing | 1031 |
| Operações | 1024 |
| Vendas | 1015 |
| Finanças | 972 |
| Não informado | 18 |

Distribuição por cargo:

| Cargo | Funcionários |
| --- | --- |
| Analista Jr | 1601 |
| Analista Pl | 1574 |
| Assistente | 1149 |
| Analista Sr | 1017 |
| Coordenador | 540 |
| Gerente | 220 |
| Diretor | 62 |

## 4. Média salarial por área

A média salarial geral dos funcionários ativos com salário válido é **R$ 6.498,45**. As médias por departamento são:

| departamento | Salário médio (R$) | Registros válidos |
| --- | --- | --- |
| Operações | 7183.95 | 1020 |
| Recursos Humanos | 7066.02 | 1042 |
| Finanças | 6698.64 | 970 |
| Tecnologia | 6468.34 | 1058 |
| Não informado | 6120.96 | 18 |
| Marketing | 5857.55 | 1028 |
| Vendas | 5721.99 | 1014 |

Operações apresenta a maior média e Vendas a menor. As diferenças são descritivas e podem refletir a composição de cargos e níveis de cada departamento; não devem ser interpretadas isoladamente como desigualdade salarial.

## 5. Extremos de remuneração por cargo

Entre os funcionários ativos, estes são os cinco cargos com menores e maiores médias salariais. A quantidade de funcionários é apresentada para contextualizar cada média.

| Cargo | Salário médio (R$) | Funcionários |
| --- | --- | --- |
| Diretor | 26143.17 | 62 |
| Gerente | 15642.74 | 220 |
| Coordenador | 10525.28 | 539 |
| Analista Sr | 10137.67 | 1015 |
| Analista Pl | 6187.42 | 1571 |
| Analista Jr | 3886.49 | 1597 |
| Assistente | 2629.27 | 1146 |

A base possui sete cargos; por isso, os grupos de cinco maiores e cinco menores se sobrepõem, e cada cargo aparece apenas uma vez na tabela.

## 6. Evolução salarial

Foi escolhido o **nível hierárquico 3**. Para cada ano, foi considerado o registro mais recente de cada funcionário naquele ano, evitando contar duas vezes a mesma pessoa no caso de dois snapshots anuais.

| ano | Salário médio (R$) | Registros |
| --- | --- | --- |
| 2018 | 5286.35 | 385 |
| 2019 | 5259.65 | 770 |
| 2020 | 5778.28 | 1076 |
| 2021 | 6317.5 | 1346 |
| 2022 | 6173.11 | 1617 |
| 2023 | 6296.97 | 1836 |

A média passou de **R$ 5.286,35** em 2018 para **R$ 6.296,97** em 2023, aumento nominal de **19.1%**. Isso não desconta inflação e a composição do grupo pode mudar ao longo dos anos; portanto, não equivale a uma comparação salarial dos mesmos indivíduos.

## 7. Rotatividade

Os desligamentos foram contados uma única vez por funcionário, pelo ano da data de desligamento.

| Ano | Desligamentos |
| --- | --- |
| 2018 | 159 |
| 2019 | 463 |
| 2020 | 615 |
| 2021 | 806 |
| 2022 | 873 |
| 2023 | 1075 |

O maior número observado ocorreu em **2023**, com **1,075 desligamentos**. Como o conjunto termina em 2023, os números dependem do período coberto e não devem ser projetados automaticamente para anos posteriores.

Admissões por ano, contadas uma vez por funcionário:

| Ano | Admissões |
| --- | --- |
| 2018 | 1683 |
| 2019 | 1740 |
| 2020 | 1648 |
| 2021 | 1620 |
| 2022 | 1694 |
| 2023 | 1743 |

## 8. Tempo de casa e promoções

O tempo de empresa foi calculado da admissão até o desligamento; para quem não tem data de desligamento, até a referência mais recente. Foram usados os valores acumulados de promoções do último registro disponível de cada funcionário.

| faixa_tempo | media_promocoes | funcionarios |
| --- | --- | --- |
| 0 a menos de 2 | 0.11 | 5533 |
| 2 a menos de 5 | 0.34 | 3880 |
| 5 a menos de 10 | 0.51 | 715 |

A correlação entre tempo de empresa e promoções acumuladas é **0.29**, indicando associação positiva nesta base. As médias por faixa também tendem a aumentar com o tempo de casa. Isso não prova que o tempo, sozinho, cause promoções: nível, função e oportunidades também podem influenciar. Datas de admissão inválidas não entram no cálculo do tempo.

## 9. Avaliação de desempenho

Média das avaliações por departamento, entre ativos no último snapshot:

| departamento | Avaliação média | Funcionários |
| --- | --- | --- |
| Não informado | 4.06 | 18 |
| Vendas | 3.78 | 1015 |
| Recursos Humanos | 3.78 | 1043 |
| Operações | 3.77 | 1024 |
| Marketing | 3.76 | 1031 |
| Tecnologia | 3.76 | 1060 |
| Finanças | 3.75 | 972 |

Média por nível hierárquico:

| nivel_hierarquico | Avaliação média | Funcionários |
| --- | --- | --- |
| 1 | 3.76 | 1149 |
| 2 | 3.76 | 1601 |
| 3 | 3.75 | 1574 |
| 4 | 3.77 | 1017 |
| 5 | 3.82 | 540 |
| 6 | 3.88 | 220 |
| 7 | 3.79 | 62 |

Entre os departamentos informados, as médias variam pouco: de **3.75** a **3.78**. O grupo “Não informado” tem 18 pessoas e média de 4.06, então não pode ser atribuído a uma área específica. O nível 6 apresenta média maior, mas possui menos pessoas que os níveis mais numerosos. Médias não demonstram, por si só, diferença estatisticamente significativa.

## 10. Gráficos e interpretações

### Quadro por departamento

![Funcionários ativos por departamento](resultados_analise_final/quadro_por_departamento.png)

O gráfico compara a quantidade de funcionários ativos por departamento no snapshot mais recente; não soma registros históricos.

### Salário por departamento

![Salário médio por departamento](resultados_analise_final/salario_por_departamento.png)

Mostra as diferenças de salário médio entre áreas, considerando apenas funcionários ativos e salários positivos.

### Extremos salariais por cargo

![Extremos de salário por cargo](resultados_analise_final/extremos_salariais_por_cargo.png)

Destaca os cinco cargos com menores e maiores remunerações médias no quadro atual.

### Evolução salarial do nível 3

![Evolução salarial do nível hierárquico 3](resultados_analise_final/evolucao_salarial_nivel_3.png)

Mostra a evolução anual da média salarial do nível escolhido, com uma observação sobre composição e inflação na questão 6.

### Desligamentos por ano

![Desligamentos por ano](resultados_analise_final/desligamentos_por_ano.png)

Permite localizar o ano com mais desligamentos identificados na base.

### Promoções e tempo de empresa

![Promoções por tempo de empresa](resultados_analise_final/promocoes_por_tempo_de_empresa.png)

Compara as promoções acumuladas médias entre faixas de tempo de casa.

### Avaliação por departamento

![Avaliação por departamento](resultados_analise_final/avaliacao_por_departamento.png)

Compara as avaliações médias dos departamentos no quadro ativo mais recente.

## 11. Estudo aplicado — retenção de talentos

**Pergunta gerencial:** os colaboradores desligados apresentam salário, desempenho ou histórico de promoções menores que os colaboradores que permaneceram?

**Passos da análise:** foi selecionado o registro mais recente de cada funcionário; os grupos foram separados pelo status nesse registro. Em seguida, foram comparados salário médio, avaliação, promoções acumuladas e tempo de empresa. O salário considera apenas valores positivos; tempo de casa usa as datas disponíveis.

| Situação | Funcionários | Salário médio (R$) | Avaliação média | Promoções médias | Tempo de empresa médio (anos) |
| --- | --- | --- | --- | --- | --- |
| Ativo | 6164 | 6498.52 | 3.77 | 0.25 | 2.48 |
| Desligado | 3991 | 6786.32 | 3.76 | 0.19 | 1.56 |

![Comparação de indicadores por status](resultados_analise_final/comparacao_retencao.png)

**Conclusão executiva:** os desligados têm avaliação média de 3.76, muito próxima da média de 3.77 dos ativos, e salário médio maior (R$ 6.786,32 contra R$ 6.498,52). Já a média de promoções é menor entre os desligados (0.19 contra 0.25, cerca de 23% a menos). Isso sugere investigar oportunidades de carreira e critérios de promoção como uma hipótese de retenção, mas não permite afirmar que a falta de promoção causou os desligamentos. Recomenda-se analisar as saídas por cargo e nível, revisar trilhas de carreira e complementar a análise com entrevistas de desligamento antes de definir uma política ampla de remuneração.

## Como reproduzir

No terminal, a partir desta pasta, instale as dependências do `requirements.txt` e execute:

```bash
python main.py
```

O programa gera este relatório e os gráficos em `resultados_analise_final/`.
