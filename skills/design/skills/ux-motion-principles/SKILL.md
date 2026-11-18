---
name: ux-motion-principles
description: >-
  Use quando for pedido para melhorar a usabilidade, a experiência, as animações, as transições ou o "feel" de um site, página, componente de interface ou apresentação de slides (HTML, Reveal.js, Marp, PowerPoint, Keynote, Google Slides), ou para revisar se uma interface ou um deck está agradável, rápido e fácil de usar. Também quando aparecerem animações lentas, exageradas ou que distraem, botões pequenos ou difíceis de clicar, menus e planos com opções demais, formulários que rejeitam o que a pessoa digita, falta de feedback ao clicar ou ao carregar, ou slides sobrecarregados. Cobre os 12 princípios de animação da Disney aplicados a UI, as leis de Fitts, Hick, Miller, Doherty, Postel e Jakob, área de toque e frequência de uso.
allowed-tools:
  - Read(~/.claude/plugins/**/caramelo-skills/**)
  - AskUserQuestion
---

# Princípios de UX e animação

Audita e melhora sites e slides passando pelos 20 princípios abaixo, um a um, e entrega o arquivo melhorado e um relatório com uma linha por princípio. A ideia central: **movimento e layout existem para a tarefa da pessoa**. Na dúvida, menos movimento e mais rápido.

A referência completa de cada princípio (o que é, como aplicar em site e em slides, valores, erros comuns e fontes) está em `references/principles.md`, relativo à pasta desta skill. Consulte a seção do princípio quando precisar de detalhe ou de exemplo de código.

## Passo 1 - Contexto

Antes de mudar qualquer coisa, identifique e anote no relatório:

- **Meio:** site/app ou slides (HTML, Reveal.js, Marp, PowerPoint/Keynote/Google Slides).
- **Tipo:** produto usado todo dia (app, painel, ferramenta) ou página vista poucas vezes (marketing, landing, deck). O tipo define o orçamento de movimento (Passo 3).
- **Gatilho de cada animação:** carga da página, clique, hover, teclado, scroll ou automática.

## Passo 2 - Auditoria: os 20 princípios

Passe por **todas** as linhas da tabela, na ordem. Para cada uma, procure o sinal no arquivo e aplique a correção. Uma linha sem problema vira "ok" no relatório; nenhuma linha fica de fora.

| #   | Princípio            | Sinal a procurar                                                                                                                          | Correção                                                                                                                    |
| --- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1   | Squash & stretch     | Botões sem estado `:active`; bounces elásticos com overshoot grande                                                                       | `:active { transform: scale(0.97) }` em 100 a 160 ms; tirar overshoot exagerado                                             |
| 2   | Anticipation         | Controles sem `:hover` e `:focus-visible`; tooltips sem atraso inicial                                                                    | Hover e foco visíveis em 100 a 150 ms; tooltip com atraso de cerca de 400 ms                                                |
| 3   | Staging              | Vários elementos animando ao mesmo tempo; ação principal sem destaque; slide com mais de uma ideia                                        | Uma coisa se move por vez; CTA principal em destaque; uma ideia por slide, título como conclusão                            |
| 4   | Pose to pose         | Keyframes com poses que não existem na UI (`scale(0) rotate(-180deg)`)                                                                    | Transição entre estados reais (fechado e aberto), com scale de 0.95 a 1 e opacity                                           |
| 5   | Follow through       | Stagger de 100 ms ou mais por item; lista que demora para terminar de entrar                                                              | Stagger de 30 a 50 ms, com o total abaixo de cerca de 300 ms                                                                |
| 6   | Slow in & slow out   | `ease-in` ou `linear` em entradas; `ease-in-out` em resposta a clique                                                                     | Entradas e respostas com ease-out; saídas mais curtas; linear só em spinner e progresso                                     |
| 7   | Moving in arcs       | Elementos que entram e saem por direções sem relação com a origem                                                                         | Coerência espacial (entra e sai pelo mesmo lado); arco só em movimentos longos                                              |
| 8   | Secondary action     | Ação concluída sem confirmação visual; efeito secundário maior que a ação                                                                 | Detalhe curto que confirma (check, contador); nunca maior que a ação principal                                              |
| 9   | Snappy timing        | Durações fora do orçamento do Passo 3                                                                                                     | Ajustar ao orçamento                                                                                                        |
| 10  | Exaggerated feedback | Clique sem resposta visível; erro indicado só por cor                                                                                     | Estados de pressionado, carregando, sucesso e erro; mensagem de erro em texto, junto do campo                               |
| 11  | Solid drawing        | Sombras com direções diferentes; elevação incoerente; gráficos 3D                                                                         | Uma fonte de luz; escala de sombras por elevação; gráficos 2D                                                               |
| 12  | Overall appeal       | Cada componente com curva e duração próprias                                                                                              | Tokens de movimento únicos (`--ease-*`, `--duration-*`); no máximo 2 tipos de transição num deck                            |
| 13  | Fitts's law          | Ação seguinte longe da anterior (submit no topo); ação destrutiva colada na frequente                                                     | Botão de envio logo após o último campo; destrutiva afastada, com estilo de perigo e confirmação ou desfazer                |
| 14  | Bigger hit areas     | Alvos clicáveis com menos de 24 px; controles importantes com menos de 44 px; texto de botão abaixo de 14 px                              | Mínimo de 24 px sempre e 44 px nos controles importantes, aumentando com `padding` ou `::after`                             |
| 15  | Hick's law           | Mais de 5 a 7 opções equivalentes sem destaque (planos, menu, CTAs)                                                                       | Destacar a recomendada, agrupar ou revelar aos poucos (veja "Decisões de produto")                                          |
| 16  | Miller's law         | Códigos ou números com mais de 6 caracteres sem separação; instruções em parágrafo; slide com mais de 5 itens                             | Grupos de 3 ou 4 caracteres; passos em lista numerada; dividir ou agrupar com subtítulos                                    |
| 17  | Doherty threshold    | Ação que espera rede ou processamento sem indicador; botão que pode ser clicado de novo                                                   | Feedback em até 100 ms; acima de 400 ms, spinner, skeleton ou progresso; desabilitar o botão                                |
| 18  | Postel's law         | `pattern` rígido, máscaras obrigatórias, mensagem "somente números"                                                                       | Aceitar variações (espaço, hífen, parênteses), normalizar e só então validar; `type`, `inputmode` e `autocomplete` corretos |
| 19  | Jakob's law          | Logo que não leva à home; carrinho ou conta fora do canto superior direito; busca escondida no desktop; Esc que não fecha; deck sem setas | Seguir a convenção correspondente                                                                                           |
| 20  | Frequency of use     | Animação em algo disparado pelo teclado ou visto muitas vezes (paleta de comandos, atalhos, toolbar, navegação por setas, hover de lista) | Aplicar as regras de frequência do Passo 3                                                                                  |

Além das 20 linhas, confira sempre os dois itens transversais, que também entram no relatório:

- **Movimento reduzido:** existe `@media (prefers-reduced-motion: reduce)` trocando deslocamento e zoom por fade curto ou nada, sem desligar spinners e barras de progresso.
- **Desempenho:** só `transform` e `opacity` são animados. Nada de `transition: all` nem animar `top`, `left`, `width`, `height` ou `margin`.

## Passo 3 - Orçamento de movimento

Regras fixas, decididas pelo gatilho e pela frequência:

| Situação                                                                      | Regra                                                                                                                   |
| ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Disparada pelo teclado (atalho, Ctrl/Cmd+K, setas, Enter, Esc) em site ou app | **Sem animação**: abre, fecha e move na hora                                                                            |
| Troca de slide pelo teclado ou passador (setas, espaço, Page Up/Down)         | Mesma transição do clique (linha "Slides: transição"): passadores enviam teclas, então é assim que o deck é apresentado |
| Vista dezenas de vezes por sessão (hover de lista, abas, toolbar, menu)       | 0 a 150 ms, só cor ou opacity                                                                                           |
| Feedback de clique (press, checkbox, toggle)                                  | 100 a 160 ms                                                                                                            |
| Tooltip, popover, dropdown                                                    | 125 a 250 ms, ease-out                                                                                                  |
| Modal, drawer, troca de tela                                                  | 200 a 300 ms, ease-out; saída cerca de 20% mais curta                                                                   |
| Movimento grande em tela grande                                               | Até 400 ms; acima disso, só com justificativa no relatório                                                              |
| Entrada na carga da página (hero)                                             | Um único fade ou deslocamento curto, total até 300 ms, ou nada                                                          |
| Slides: transição entre slides                                                | 200 a 300 ms, um único tipo no deck inteiro (fade ou push)                                                              |
| Slides: revelação de item ou de gráfico                                       | 150 a 300 ms por clique; o gráfico revela o destaque, não cresce barra por barra                                        |
| Página de marketing vista uma vez                                             | Pode passar desses valores só nos momentos de destaque, nunca em controles                                              |

Curvas: ease-out `cubic-bezier(0.2, 0, 0, 1)` para entradas e respostas; ease-in `cubic-bezier(0.3, 0, 1, 1)` para saídas; ease-in-out `cubic-bezier(0.65, 0, 0.35, 1)` para movimento dentro da tela. Declare tudo como tokens em `:root` e use os tokens em todo o arquivo.

## Decisões de produto

Algumas correções mudam o produto, como reduzir planos, reorganizar o menu, remover conteúdo ou tirar um dado sensível da página. Para cada uma, faça uma das duas coisas e registre no relatório qual foi:

- **Correção que mantém todo o texto original:** aplique. Isso inclui reorganizar: destacar um plano como "Recomendado", agrupar o menu em categorias com submenus, agrupar um código em blocos, deixar a busca visível, dividir um slide sobrecarregado em dois, transformar parágrafo em lista e mover itens para grupos com subtítulo.
- **Correção que remove texto, reescreve frases ou muda dados** (cortar planos, trocar o título por outra frase, tirar um item): não aplique. Escreva no relatório a proposta concreta, com o que muda e por quê (ex: "Reduzir de 9 para 4 planos: Free, Plus, Pro e Business; os outros viram faixas dentro desses").

"É decisão de negócio" nunca é o conteúdo inteiro da linha: toda linha de decisão de produto tem uma proposta concreta.

## Passo 4 - Verificação

Antes de entregar, confira no arquivo final:

1. Cada `transition` e `animation` está dentro do orçamento do Passo 3. Procure com Grep por `ms`, `s;`, `s ` e `animation-delay` e some os atrasos de stagger.
2. Nenhuma entrada usa `ease-in` nem `linear`.
3. Nenhum handler de teclado (`keydown`) abre algo com animação.
4. Existe `prefers-reduced-motion`.
5. Nenhum `transition: all`, e nenhuma animação de `top`, `left`, `width`, `height` ou `margin`.
6. Todos os controles clicáveis têm pelo menos 24 px, e os importantes 44 px.
7. Se houver navegador disponível, abra o arquivo e teste clique, teclado e movimento reduzido. Se não houver, diga no relatório que a verificação foi só pelo código.

## Passo 5 - Relatório

Entregue, nesta ordem:

1. **Contexto:** meio, tipo e o orçamento usado.
2. **Tabela dos 20 princípios**, com as 20 linhas sempre presentes, mais as linhas de movimento reduzido e de desempenho:

   | #   | Princípio        | Status                                    | O que foi feito ou proposto |
   | --- | ---------------- | ----------------------------------------- | --------------------------- |
   | 1   | Squash & stretch | corrigido / ok / proposta / não se aplica | ...                         |

   `não se aplica` só quando o meio não tem o elemento (ex: Postel num deck sem campos). `proposta` é para as decisões de produto e sempre traz a mudança concreta.

3. **Decisões para a pessoa:** as propostas que dependem dela, em lista curta.
4. **Como foi verificado:** navegador ou só código.

## Erros comuns

| Erro                                                                      | Por que é errado                                                                         |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Trocar uma animação de 800 ms por uma de 420 ms e considerar resolvido    | Continua fora do orçamento; a referência para modal é 200 a 300 ms                       |
| Deixar a paleta de comandos ou um atalho com fade "curtinho"              | Ação de teclado repetida muitas vezes; qualquer animação vira atraso                     |
| Pular planos, menu ou conteúdo extenso dizendo que "é decisão de negócio" | A pessoa fica sem proposta; destacar e agrupar não removem nada e podem ser aplicados    |
| Corrigir tamanho de botão e esquecer o estado `:active`                   | Sem resposta ao clique, a interface parece travada                                       |
| Barra de gráfico que cresce em 700 ms ou mais                             | A plateia espera a animação terminar; o destaque deve aparecer, não demorar              |
| Ajustar só o que estava claramente quebrado                               | Os princípios 15, 16 e 19 costumam passar batido; a tabela do relatório existe para isso |
