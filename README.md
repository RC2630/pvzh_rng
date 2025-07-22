# Plants vs. Zombies Heroes - Random Number Generator

### Here is a list of available commands:
- `/draw`: draw 1 card
- `/draw <count>`: draw `count` cards
- `/conjure <key:value...> <amphibious?> <gravestone?> <superpower?>`: conjure 1 card
- `/conjure <key:value...> <amphibious?> <gravestone?> <superpower?> <count>`: conjure `count` cards
- `/ping`: hit the hero once (returns the increase in super block meter charges)
- `/block`: give the superpower obtained when the hero super-blocks
- `/shuffle <card> <copies>`: shuffle `copies` copies of `card` into the deck
- `/start`: start the match (initial 4 cards + redraws + initial superpower)
- `/end`: end the match (and terminates the program)
- `/randint <max>`: generate a random integer between 1 and `max` (inclusive)

### Details on conjuring:
The command `/conjure` conjures 1 or more cards based on the following parameters:
- `side:<side>` to specify which side the conjured card belongs to (ex. `side:zombie`)
- `tribe:<tribe>` or `tribe:<tribe1>|<tribe2>|<...>` to specify that the conjured card must be of a certain tribe or one of several tribes (ex. `tribe:fruit`, `tribe:flower|berry`)
- `set:<set>` to specify the set (expansion pack) of the conjured card (ex. `set:galactic`)
- `type:<type>` to specify the type (minion, trick, or environment) of the conjured card (ex. `type:trick`)
- `cost:<cost>` or `cost:<=<cost>` or `cost:>=<cost>` to specify the exact, maximum, or minimum cost of the conjured card (ex. `cost:2`, `cost:>=5`)
- `rarity:<rarity>` to specify the rarity of the conjured card (ex. `rarity:legendary`)
- an optional flag `amphibious` to specify that the conjured card has the amphibious trait
- an optional flag `gravestone` to specify that the conjured card has the gravestone trait
- an optional flag `superpower` to specify that the conjured card is a superpower (without this flag, superpowers will never be conjured)
- an optional count (ex. `3`) at the end to specify the number of cards to conjure (the default is 1)

Examples of `/conjure` commands:
- `/conjure side:zombie 3`: conjure any 3 zombie cards (Eureka)
- `/conjure tribe:corn|squash|bean`: conjure a corn, squash, or bean (Mayflower)
- `/conjure side:plant set:galactic`: conjure a galactic card (Photosynthesizer)
- `/conjure side:plant type:trick 2`: conjure 2 tricks (Lightspeed Seed)
- `/conjure side:plant cost:>=4`: conjure a card that costs 4 or more (Primal Wall-Nut)
- `/conjure side:zombie rarity:legendary`: conjure a legendary card (Buried Treasure)
- `/conjure tribe:imp cost:<=2 amphibious`: conjure (make) an amphibious imp that costs 2 or less (Imp-Throwing Imp, when throwing to the water lane)
- `/conjure gravestone`: conjure (make) a gravestone (Tomb Raiser Zombie)
- `/conjure side:zombie superpower 2`: conjure 2 superpowers (Thinking Cap)
- `/conjure side:plant type:minion`: conjure (make) a plant (Cornucopia)

### Here is an example of the deck format used in `input/deck.txt`:
> Green Shadows
>
> Snowdrop 4
>
> Snow Pea 4
>
> Chilly Pepper 4
>
> Iceburg Lettuce 4
>
> Winter Squash 4
>
> Winter Melon 4
>
> Cool Bean 4
>
> Jolly Holly 4
>
> Lily Pad 2
>
> Umbrella Leaf 2
>
> Coffee Grounds 2
>
> Plant Food 2