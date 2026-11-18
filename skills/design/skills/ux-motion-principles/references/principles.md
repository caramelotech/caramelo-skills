# Os 20 princípios de UX e animação

Referência detalhada da skill `ux-motion-principles`. Cada princípio tem: o que é, como aplicar em sites, como aplicar em slides, valores de partida e o erro mais comum. Os números são pontos de partida para testar, não leis: quando as fontes divergem, isso está indicado.

Os princípios 1 a 12 vêm dos 12 princípios de animação da Disney (Ollie Johnston e Frank Thomas, _The Illusion of Life_, 1981), adaptados para interfaces. Os 13 a 19 são leis de UX da psicologia e da engenharia. O 20 é um critério de produto para decidir quanto animar.

## Sumário

| #   | Princípio            | Pergunta que ele responde                                  |
| --- | -------------------- | ---------------------------------------------------------- |
| 1   | Squash & stretch     | O elemento parece físico e responde ao toque?              |
| 2   | Anticipation         | A pessoa sabe o que vai acontecer antes de agir?           |
| 3   | Staging              | Para onde o olho vai primeiro?                             |
| 4   | Pose to pose         | Os estados inicial e final estão bem definidos?            |
| 5   | Follow through       | As partes relacionadas chegam em ordem e com hierarquia?   |
| 6   | Slow in & slow out   | A curva de easing é natural e responsiva?                  |
| 7   | Moving in arcs       | O caminho do movimento parece orgânico e tem origem clara? |
| 8   | Secondary action     | Há um detalhe que reforça a ação principal sem competir?   |
| 9   | Snappy timing        | A duração é a menor possível sem ficar abrupta?            |
| 10  | Exaggerated feedback | O resultado da ação é impossível de não perceber?          |
| 11  | Solid drawing in 3D  | Luz, sombra, profundidade e perspectiva são coerentes?     |
| 12  | Overall appeal       | O conjunto tem personalidade e consistência?               |
| 13  | Fitts's law          | O alvo está perto e grande o bastante?                     |
| 14  | Bigger hit areas     | A área clicável é maior que o ícone visível?               |
| 15  | Hick's law           | Há opções demais para decidir rápido?                      |
| 16  | Miller's law         | A informação está agrupada em blocos que cabem na memória? |
| 17  | Doherty threshold    | O sistema responde em menos de 400 ms?                     |
| 18  | Postel's law         | A entrada aceita as variações que as pessoas digitam?      |
| 19  | Jakob's law          | Funciona como os sites que a pessoa já conhece?            |
| 20  | Frequency of use     | Quantas vezes por dia a pessoa vê essa animação?           |

## 1. Squash & stretch

**O que é.** Deformar um objeto ao bater, apertar ou acelerar comunica peso, massa e flexibilidade. Na Disney, o volume se mantém: o que estica afina, o que achata alarga.

**Em sites.** O uso principal é o feedback de pressão: um botão que encolhe levemente no `:active` parece físico. Também vale para um ícone que "pula" ao receber uma notificação.

**Em slides.** Raramente se aplica. No máximo, um ícone ou número que pulsa uma vez para marcar o dado principal.

**Valores de partida.** `transform: scale(0.97)` no `:active`, 100 a 160 ms. Deformações não uniformes (só no eixo X ou Y) ficam entre 2% e 5%.

**Erro comum.** Bounce elástico em tudo (`cubic-bezier` com overshoot grande). Em UI, o exagero cansa e parece amador.

## 2. Anticipation (wind-up)

**O que é.** Um pequeno movimento preparatório avisa o que vem a seguir, como o personagem que recua antes de pular.

**Em sites.** Estados de hover e foco que mostram que algo é clicável, como um botão que muda de cor, uma seta que avança alguns pixels ou um card que se eleva. Mostrar o destino antes do clique (preview, tooltip) também é antecipação.

**Em slides.** Avisar o que vem: uma agenda no início, um título que anuncia a conclusão do slide ("Enterprise puxou o crescimento") antes do gráfico.

**Valores de partida.** Hover em 100 a 150 ms. Tooltips e previews com atraso inicial (cerca de 300 a 500 ms) para não dispararem quando o cursor só passa por cima. Depois que um tooltip abre, os vizinhos abrem na hora.

**Erro comum.** Não ter `:focus-visible`. Quem navega por teclado não recebe nenhuma antecipação.

## 3. Staging (focar a atenção)

**O que é.** Apresentar uma ideia de cada vez, de forma que ela seja inequívoca. O movimento é o estímulo visual mais forte que existe, então ele decide para onde o olho vai.

**Em sites.** Só uma coisa se move de cada vez. A ação principal da tela é a mais visível. Animações de entrada em massa (todos os blocos do hero quicando) dispersam a atenção e atrasam a leitura.

**Em slides.** Uma ideia por slide. Revelar os itens por clique quando a fala acompanha, destacar o dado principal do gráfico (cor de destaque só nele, o resto em cinza) e usar o título como a conclusão.

**Valores de partida.** No máximo um elemento chamando atenção por vez. Escalonamento (stagger) entre itens de 30 a 50 ms, com o total abaixo de cerca de 300 ms.

**Erro comum.** Animar tudo na carga da página. Se tudo se mexe, nada se destaca.

## 4. Pose to pose

**O que é.** Definir as poses-chave e deixar o intervalo ser preenchido, em vez de animar quadro a quadro.

**Em sites.** Projetar os estados (fechado, abrindo, aberto, erro, carregando) antes da transição entre eles. Em CSS, são `transition` entre estados bem definidos ou `@keyframes` com poucos quadros. Morphing entre estados (botão que vira spinner, ícone de menu que vira X) é pose to pose.

**Em slides.** Transições "morph" ou "magic move" entre dois slides com o mesmo objeto em posições diferentes mostram a mudança de estado, como um número antes e depois.

**Valores de partida.** Duas a três poses por transição. Se precisar de mais, provavelmente é ilustração, não UI.

**Erro comum.** Estados intermediários sem sentido, como `scale(0) rotate(-180deg)`, onde o objeto passa por poses que não existem na interface.

## 5. Follow through & overlapping action

**O que é.** Partes diferentes de um objeto param em tempos diferentes. O cabelo continua se movendo depois que o personagem para.

**Em sites.** Quando um card abre, a imagem chega primeiro e o título e a descrição chegam logo depois. Num modal, o fundo escurece e o conteúdo entra com um pequeno atraso. Isso estabelece hierarquia.

**Em slides.** Num slide com título e gráfico, o título aparece primeiro e o gráfico em seguida, sem que cada barra tenha a própria animação longa.

**Valores de partida.** Atraso de 30 a 80 ms entre partes relacionadas. O conjunto continua cabendo no orçamento de duração do princípio 9.

**Erro comum.** Escalonamento longo (0,3 s ou mais por item), em que a pessoa espera a lista inteira terminar de entrar para ler.

## 6. Slow in & slow out (easing)

**O que é.** Objetos reais aceleram e desaceleram. Movimento linear parece mecânico.

**Em sites.**

- Entradas e qualquer resposta a uma ação: **ease-out** (começa rápido e desacelera). Parece responsivo, porque o movimento começa na hora.
- Saídas: ease-in ou ease-out mais curto. O elemento sai do caminho e ninguém espera por ele.
- Movimento de algo que já está na tela de um ponto a outro: ease-in-out.
- Linear só para rotação contínua (spinner) e barras de progresso.

**Em slides.** As mesmas curvas. As transições padrão do PowerPoint e do Keynote, como "Fade" e "Push", já usam easing; evite "Bounce", "Spin" e "Swivel".

**Valores de partida (CSS).**

```css
:root {
  --ease-out: cubic-bezier(0.2, 0, 0, 1); /* entering, responding */
  --ease-in: cubic-bezier(0.3, 0, 1, 1); /* leaving */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* moving on screen */
}
```

**Erro comum.** Ease-in em entradas. Um dropdown de 300 ms com ease-in parece mais lento que um de 300 ms com ease-out, porque nos primeiros quadros quase nada acontece.

## 7. Moving in arcs

**O que é.** Movimentos naturais seguem arcos, não linhas retas.

**Em sites.** Um item que voa até o carrinho ou a lixeira em curva parece orgânico e mostra a origem e o destino. Em CSS, use `offset-path` ou anime X e Y com curvas de easing diferentes. Mais importante que o arco é a **coerência espacial**: o que entra pela direita sai pela direita, e um toast que entra por baixo é dispensado com gesto para baixo.

**Em slides.** Raro. Útil para mostrar fluxo (um item que se move de uma etapa para outra num diagrama).

**Valores de partida.** Só em movimentos com distância perceptível (mais de cerca de 100 px). Em movimentos curtos, o arco é imperceptível e não vale o código.

**Erro comum.** Elementos que surgem de direções aleatórias, sem relação com o lugar de onde vieram ou para onde vão.

## 8. Secondary action

**O que é.** Uma ação secundária que reforça a principal sem competir com ela, como o personagem que assobia enquanto anda.

**Em sites.** O check que aparece dentro do botão depois de salvar, o contador que incrementa ao adicionar ao carrinho, o confete depois de concluir um formulário longo (uma vez só).

**Em slides.** Um ícone pequeno ao lado do número principal, um sublinhado que se desenha sob a palavra-chave.

**Valores de partida.** Começa junto ou logo depois da ação principal e é mais curta e mais sutil que ela.

**Erro comum.** A ação secundária ficar maior que a principal (confete toda vez que algo é salvo).

## 9. Snappy timing

**O que é.** O número de quadros define a velocidade, e a velocidade define a personalidade. Em interfaces, rápido significa responsivo.

**Em sites.** Procure a menor duração que não fique abrupta. Animações longas demais são muito mais comuns que curtas demais. Pequenas diferenças (250 contra 300 ms) já são perceptíveis.

| Elemento                                   | Duração                               |
| ------------------------------------------ | ------------------------------------- |
| Feedback simples (checkbox, toggle, press) | cerca de 100 ms (100 a 160)           |
| Hover, tooltip, popover pequeno            | 125 a 200 ms                          |
| Dropdown, select, menu                     | 150 a 250 ms                          |
| Modal, mudança grande de tela              | 200 a 300 ms                          |
| Movimento grande em telas grandes, drawer  | até 400 ms (500 é o teto)             |
| Saída                                      | cerca de 20% mais curta que a entrada |

Fora de sites de marketing, UI fica abaixo de 300 ms.

**Em slides.** Transições entre slides de 200 a 400 ms. Revelação de itens de 150 a 300 ms. A plateia espera a animação terminar para olhar para quem fala, então cada segundo de animação é um segundo de atenção perdida.

**Erro comum.** Durações de 600 ms a 1,5 s "para ficar suave". Ficam lentas, não suaves.

## 10. Exaggerated feedback

**O que é.** Exagerar um pouco o movimento para que a ação fique clara. Na UI, o exagero está no feedback: o resultado de cada ação precisa ser impossível de não perceber.

**Em sites.** Todo clique tem resposta visível: estado pressionado, carregando, sucesso e erro. Erros com texto que diz o que fazer, perto do campo, e não só com uma borda vermelha (cor sozinha não basta para daltônicos). Um campo inválido pode tremer uma vez (cerca de 300 ms) para chamar atenção.

**Em slides.** Exagero de contraste, não de movimento: o número principal grande, a palavra-chave em cor de destaque.

**Valores de partida.** O feedback aparece em até 100 ms depois da ação. Tremor de erro com deslocamento de 4 a 8 px, uma vez.

**Erro comum.** Confundir exagero com efeito chamativo. O exagero que distrai irrita; uma boa animação costuma passar despercebida.

## 11. Solid drawing in 3D

**O que é.** Desenhar com volume, peso e perspectiva consistentes.

**Em sites.** Uma única fonte de luz para todas as sombras (normalmente de cima, então a sombra cai para baixo). Elevação coerente: o que está mais alto (modal, menu) tem sombra maior. Transformações 3D com `perspective` definida no pai e rotações pequenas. Ícones e ilustrações no mesmo estilo de traço e de perspectiva.

**Em slides.** Mesma fonte de luz e mesmo estilo de sombra em todas as formas. Gráficos 3D distorcem a leitura dos valores e devem ser evitados.

**Valores de partida.**

```css
:root {
  --shadow-1: 0 1px 2px rgb(0 0 0 / 0.12); /* card */
  --shadow-2: 0 4px 12px rgb(0 0 0 / 0.14); /* hover, dropdown */
  --shadow-3: 0 12px 32px rgb(0 0 0 / 0.18); /* modal */
}
```

**Erro comum.** Sombras com direções diferentes na mesma tela, o que faz a interface parecer quebrada.

## 12. Overall appeal

**O que é.** Personalidade e carisma. Não tem fórmula: vem da consistência dos outros onze princípios e de testar com pessoas.

**Em sites.** Um sistema de movimento único (as mesmas curvas e durações em tokens), coerente com o tom da marca. Um banco é sóbrio; um app para crianças pode ter mais elasticidade.

**Em slides.** No máximo um ou dois tipos de transição no deck inteiro e o mesmo estilo de revelação em todos os slides.

**Erro comum.** Cada componente com a própria curva e duração, porque cada pessoa escolheu a sua.

## 13. Fitts's law

**O que é.** O tempo para atingir um alvo depende da distância até ele e do tamanho dele. Alvos grandes e próximos são mais rápidos e geram menos erros.

**Em sites.**

- A ação seguinte fica perto da anterior: o botão de enviar logo abaixo do último campo, não no topo do formulário.
- Ícone mais rótulo forma um alvo maior que só o ícone, e a área inteira deve ser clicável.
- Com mouse, as bordas da tela funcionam como paredes (alvos infinitos em um eixo). No toque isso não vale.
- Não amontoe alvos: espaço entre eles evita toques errados.
- Ações destrutivas ficam longe das frequentes e com estilo diferente, de preferência com confirmação ou desfazer.

**Em slides.** Os controles de navegação de um deck em HTML (anterior, próximo) precisam ser grandes ou ocupar as laterais da tela. Também é bom aceitar teclado (setas, espaço, Page Up e Page Down, que os passadores de slide usam).

**Erro comum.** Botões pequenos com texto de 11 px, e o botão de excluir colado no de salvar.

## 14. Bigger hit areas

**O que é.** A área clicável pode e deve ser maior que o elemento visível.

**Em sites.**

| Referência                   | Tamanho mínimo                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------- |
| WCAG 2.2, 2.5.8 (AA)         | 24 x 24 px CSS, ou espaçamento que garanta um círculo de 24 px sem sobreposição |
| WCAG 2.5.5 (AAA)             | 44 x 44 px CSS                                                                  |
| Apple HIG                    | 44 x 44 pt                                                                      |
| Material Design              | 48 x 48 dp                                                                      |
| Nielsen Norman Group (toque) | cerca de 1 cm                                                                   |

Use 44 px como padrão para controles importantes e nunca menos de 24 px. Aumente a área com `padding` ou com um pseudo-elemento, sem mudar o tamanho do ícone:

```css
.icon-button {
  position: relative;
  inline-size: 24px;
  block-size: 24px;
}
.icon-button::after {
  content: "";
  position: absolute;
  inset: -10px; /* 24 + 2 * 10 = 44px hit area */
}
```

Uma área estendida invisível ainda faz a pessoa mirar na borda visível. Quando der, deixe a área perceptível (fundo no hover, padding visível).

**Erro comum.** Ícones de 16 a 18 px clicáveis só no glifo.

## 15. Hick's law

**O que é.** O tempo de decisão cresce com o número e a complexidade das opções (Hick e Hyman, 1952).

**Em sites.** Reduza as opções quando o tempo de resposta importa. Destaque uma opção recomendada, divida tarefas complexas em etapas e use revelação progressiva (mostrar o avançado só quando pedido). Uma tabela de planos funciona melhor com três ou quatro opções e uma marcada como recomendada.

**Em slides.** Uma pergunta ou decisão por slide. Opções comparadas lado a lado, com a recomendada em destaque.

**Limite.** Não simplifique até perder o sentido. Para listas que a pessoa já conhece e ordena (países, nomes), o tempo cresce pouco, e busca ou ordenação ajudam mais que cortar itens.

**Erro comum.** Esconder opções importantes para "limpar" a tela, o que troca tempo de decisão por tempo de procura.

## 16. Miller's law

**O que é.** A memória de trabalho guarda poucos itens por vez. Miller (1956) falou em 7 mais ou menos 2; pesquisas posteriores (Cowan, 2001) indicam cerca de 4 blocos (chunks).

**Em sites.** Agrupe (chunking): códigos e números longos em grupos de 3 ou 4 caracteres, passos em lista numerada, formulários longos em seções com título. Não use "7" como limite arbitrário de itens de menu: menus são reconhecimento, não memorização.

**Em slides.** Três a cinco itens por slide. Mais que isso vira dois slides ou um agrupamento com subtítulos.

**Erro comum.** Parágrafo único com dez instruções em sequência, ou um código de 16 caracteres sem separação.

## 17. Doherty threshold

**O que é.** A produtividade dispara quando sistema e pessoa interagem num ritmo (abaixo de 400 ms) em que nenhum espera pelo outro (Doherty e Thadani, IBM, 1982).

**Limites de tempo de resposta (Nielsen):** até 0,1 s parece instantâneo; até 1 s mantém o fluxo de pensamento; acima de 10 s a atenção se perde.

**Em sites.**

- Feedback de que a ação foi recebida em até 100 ms (estado pressionado, botão desabilitado com "Enviando...").
- Se a resposta passar de cerca de 400 ms, mostre progresso: spinner para esperas curtas, skeleton para conteúdo que está carregando e barra de progresso com tempo estimado para esperas longas.
- UI otimista: mostre o resultado na hora e reverta se o servidor falhar.
- Animações rápidas ajudam a percepção de desempenho; animações lentas fazem tudo parecer lento.

**Em slides.** A fala não espera a animação. Se uma revelação demora mais que cerca de 400 ms, quem apresenta fica parado esperando.

**Erro comum.** Botão de enviar que não muda nada por 2 segundos, fazendo a pessoa clicar de novo.

## 18. Postel's law

**O que é.** "Seja liberal no que aceita e conservador no que envia" (Jon Postel, TCP). Também chamado de princípio da robustez.

**Em sites.** Aceite as variações que as pessoas digitam e normalize: telefone com ou sem parênteses, espaços e hífens; CEP com ou sem hífen; datas com seletor nativo ou parse tolerante; e-mail com espaços nas pontas. Valide depois de normalizar, mostre o valor interpretado e, quando não der para entender, diga exatamente o formato esperado. Use `type`, `inputmode` e `autocomplete` corretos para ajudar o teclado e o preenchimento automático.

```js
const digitsOnly = (value) => value.replace(/\D/g, "");
const phone = digitsOnly(input.value); // "(81) 99999-0000" -> "81999990000"
```

**Em slides.** Aceite os comandos que os passadores enviam (setas, espaço, Page Up e Page Down, clique) e funcione bem em telas de tamanhos diferentes.

**Erro comum.** `pattern="\d{11}"` com mensagem "somente números", rejeitando o que a pessoa digitou de forma perfeitamente compreensível.

## 19. Jakob's law

**O que é.** As pessoas passam a maior parte do tempo em outros sites e esperam que o seu funcione como eles (Jakob Nielsen).

**Em sites.** Siga as convenções: logo no canto superior esquerdo levando para a página inicial, busca visível no topo, carrinho e conta no canto superior direito, links com aparência de link, X para fechar no canto superior direito do modal, Esc fecha modais e menus. Em redesenhos, mude aos poucos e, se possível, deixe a pessoa voltar à versão antiga por um tempo.

**Em slides.** Convenções de apresentação: título no topo, numeração no canto, setas e espaço avançam, Esc sai da tela cheia.

**Erro comum.** Inventar navegação "criativa" (carrinho à esquerda, busca escondida no menu hambúrguer no desktop).

## 20. Frequency of use

**O que é.** Quanto mais vezes alguém vê uma animação, menos ela deve animar. O encanto some com a repetição e a demora fica.

**Como decidir.**

| Frequência                                           | Exemplo                                                            | Animação                                |
| ---------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------- |
| Centenas de vezes por dia, ou disparada pelo teclado | Paleta de comandos, atalhos, navegação por setas, itens de toolbar | Nenhuma (instantânea)                   |
| Dezenas de vezes por dia                             | Hover, menus, abas, dropdowns                                      | Mínima, 100 a 200 ms, ou nenhuma        |
| Ocasional                                            | Modais, toasts, popovers                                           | Curta, 150 a 250 ms, ease-out           |
| Rara ou única                                        | Onboarding, conclusão de cadastro, marketing                       | Pode ter personalidade e ser mais longa |

**Regra para teclado.** Ações disparadas pelo teclado nunca são animadas: o destaque numa lista acompanha a seta na hora.

**Em slides.** O deck é visto uma vez, mas cada revelação se repete dezenas de vezes na mesma apresentação. Uma animação que diverte no primeiro slide cansa no décimo.

**Erro comum.** Animar com bounce a paleta de comandos que a pessoa abre o dia inteiro.

## Acessibilidade e desempenho (valem para todos)

- **Movimento reduzido.** Respeite `prefers-reduced-motion: reduce` (técnica C39 do W3C; a WCAG 2.3.3 é AAA). Troque deslocamentos, zoom e parallax por fade curto ou nenhuma animação. Não desligue indicadores funcionais (spinner, barra de progresso): reduza-os.
- **Nada pisca** mais de três vezes por segundo (WCAG 2.3.1).
- **Movimento automático** que dura mais de 5 segundos (carrossel, vídeo de fundo) precisa de pausa (WCAG 2.2.2).
- **Desempenho.** Anime só `transform` e `opacity`, que o navegador compõe sem refazer layout. Evite animar `top`, `left`, `width`, `height`, `margin` e `transition: all`. Use `will-change` com moderação.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Fontes

- Nielsen Norman Group: [Executing UX Animations: Duration and Motion Characteristics](https://www.nngroup.com/articles/animation-duration/), [Fitts's Law and Its Applications in UX](https://www.nngroup.com/articles/fitts-law/), [Response Times: The 3 Important Limits](https://www.nngroup.com/articles/response-times-3-important-limits/)
- Laws of UX (Jon Yablonski): [Doherty Threshold](https://lawsofux.com/doherty-threshold/), [Hick's Law](https://lawsofux.com/hicks-law/), [Miller's Law](https://lawsofux.com/millers-law/), [Postel's Law](https://lawsofux.com/postels-law/), [Jakob's Law](https://lawsofux.com/jakobs-law/)
- W3C: [Understanding SC 2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [Understanding SC 2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions), [Técnica C39: prefers-reduced-motion](https://www.w3.org/WAI/WCAG22/Techniques/css/C39)
- Interaction Design Foundation: [UI Animation: How to Apply Disney's 12 Principles of Animation to UI Design](https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design)
- Emil Kowalski: [You Don't Need Animations](https://emilkowal.ski/ui/you-dont-need-animations)
- web.dev: [How to create high-performance CSS animations](https://web.dev/articles/animations-guide), [Animations and performance](https://web.dev/articles/animations-and-performance)
- Cowan, N. (2001). [The magical number 4 in short-term memory](https://pmc.ncbi.nlm.nih.gov/articles/PMC2864034/)
- MDN: [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
