# FOMO Data Sources Registry - Complete Structure

## Принцип Приоритетности
```
1. ПАРСЕР (Web scraping, RSS) - всегда работает без ключей
2. ПУБЛИЧНЫЙ API (бесплатный) - работает с лимитами
3. ПЛАТНЫЙ API (требует ключ) - опционально, расширяет данные
```

**Логика**: Если нет API ключа - используем парсер. API дополняет, но не блокирует работу.

---

## TIER 1 - КРИТИЧЕСКИ ВАЖНЫЕ (Всегда активны)
Работают через парсер/бесплатный API. Без них система не функциональна.

### Market Data
| ID | Name | Тип доступа | Статус | Описание |
|---|---|---|---|---|
| defillama | DefiLlama | API Public | ✅ Active | TVL, протоколы, chains - бесплатный API |
| dexscreener | DEXScreener | API Public | ✅ Active | DEX пары, цены - бесплатный API |
| geckoterminal | GeckoTerminal | API Public | ✅ Active | DEX pools, trending - бесплатный API |
| l2beat | L2BEAT | API Public | ✅ Active | L2 TVL, риски - бесплатный API |
| growthepie | growthepie | API Public | ✅ Active | L2 аналитика - бесплатный API |

### Intel / Funding
| ID | Name | Тип доступа | Статус | Описание |
|---|---|---|---|---|
| cryptorank | CryptoRank | Parser + API | ✅ Active | Funding rounds, VC - парсер работает |
| rootdata | RootData | Parser + API | ✅ Active | Investments, teams - парсер работает |
| icodrops | ICO Drops | Parser | ✅ Active | ICO/IDO/Launchpads - веб парсер |
| dropsearn | DropsEarn | Parser | ✅ Active | Airdrops - веб парсер |
| crunchbase | Crunchbase | Parser | ✅ Active | Funding, companies - веб парсер |

### News (RSS)
| ID | Name | Тип доступа | Статус | Описание |
|---|---|---|---|---|
| cointelegraph | Cointelegraph | RSS | ✅ Active | Tier A news |
| theblock | The Block | RSS | ✅ Active | Tier A news |
| coindesk | CoinDesk | RSS | ✅ Active | Tier A news |
| decrypt | Decrypt | RSS | ✅ Active | Tier A news |
| blockworks | Blockworks | RSS | ✅ Active | Tier A news |

---

## TIER 2 - ВАЖНЫЕ (Работают через парсер или публичный API)
Дополняют данные, но не критичны.

### DEX Analytics
| ID | Name | Тип доступа | Статус | Описание |
|---|---|---|---|---|
| dextools | DEXTools | API Trial | ⚠️ Limited | Trial API с лимитами |
| defined | Defined.fi | GraphQL | ⚠️ Limited | GraphQL API |

### Token Unlocks
| ID | Name | Тип доступа | Статус | Описание |
|---|---|---|---|---|
| tokenunlocks | TokenUnlocks | Parser + API | ⚠️ Parser | Unlock schedules |
| vestlab | VestLab | Parser | ⚠️ Parser | Vesting data |

### Derivatives
| ID | Name | Тип доступа | Статус | Описание |
|---|---|---|---|---|
| coinglass | Coinglass | API Public | ✅ Active | Funding, OI, liquidations |
| laevitas | Laevitas | API Limited | ⚠️ Limited | Options, futures |
| velodata | Velo Data | API Limited | ⚠️ Limited | Derivatives analytics |

### On-chain (Premium - парсер fallback)
| ID | Name | Тип доступа | Статус | Описание |
|---|---|---|---|---|
| nansen | Nansen | Parser | ⚠️ Parser | Wallets, flows - веб парсер |
| arkham | Arkham | Parser | ⚠️ Parser | Entity intel - веб парсер |
| dune | Dune | API Free Tier | ⚠️ Limited | Public dashboards |
| glassnode | Glassnode | API Free Tier | ⚠️ Limited | Basic metrics free |
| santiment | Santiment | GraphQL Free | ⚠️ Limited | Social, on-chain |

### Activities
| ID | Name | Тип доступа | Статус | Описание |
|---|---|---|---|---|
| dropstab | Dropstab | Parser | ⚠️ Parser | Activities - веб парсер |
| dappradar | DappRadar | Parser + API | ⚠️ Parser | DApps ranking |
| airdropalert | AirdropAlert | Parser | ⚠️ Parser | Airdrop alerts |
| artemis | Artemis | API Limited | ⚠️ Limited | Chain analytics |

---

## TIER 3 - ОПЦИОНАЛЬНЫЕ (Требуют API ключ)
Расширяют данные при наличии ключа. Без ключа - игнорируются.

### Market Data (API Key Required)
| ID | Name | API Key | Статус | Описание |
|---|---|---|---|---|
| coingecko | CoinGecko | CG_API_KEY | 🔑 Key Required | Market data, prices |
| coinmarketcap | CoinMarketCap | CMC_API_KEY | 🔑 Key Required | Market data, rankings |
| messari | Messari | MESSARI_API_KEY | 🔑 Key Required | Research, metrics |
| tokenterminal | Token Terminal | TT_API_KEY | 🔑 Key Required | Fundamentals |

---

## TIER 4 - БИРЖЕВЫЕ ИСТОЧНИКИ

### CEX (Centralized Exchanges)
| Rank | Name | Slug | Type | API | Описание |
|---|---|---|---|---|---|
| 1 | Binance | binance | CEX | Public | Largest by volume |
| 2 | Coinbase | coinbase | CEX | Public | US regulated |
| 3 | Bybit | bybit | CEX | Public | Derivatives focus |
| 4 | OKX | okx | CEX | Public | Full suite |
| 5 | Kraken | kraken | CEX | Public | US regulated |
| 6 | KuCoin | kucoin | CEX | Public | Altcoin focus |
| 7 | Gate.io | gate-io | CEX | Public | Wide listings |
| 8 | Huobi | huobi | CEX | Public | Asia focus |
| 9 | MEXC | mexc | CEX | Public | Fast listings |
| 10 | Bitget | bitget | CEX | Public | Copy trading |
| 11 | Bitfinex | bitfinex | CEX | Public | Whale market |
| 12 | Bitstamp | bitstamp | CEX | Public | EU regulated |
| 13 | Crypto.com | crypto-com | CEX | Public | Consumer app |
| 14 | Gemini | gemini | CEX | Public | US regulated |

### DEX (Decentralized Exchanges)
| Rank | Name | Slug | Chain | Type | Описание |
|---|---|---|---|---|---|
| 1 | Uniswap | uniswap | Ethereum | AMM | Largest DEX |
| 2 | dYdX | dydx | Cosmos | Orderbook | Perps |
| 3 | HyperLiquid | hyperliquid | Arbitrum | Orderbook | Perps |
| 4 | PancakeSwap | pancakeswap | BSC | AMM | BSC leader |
| 5 | Curve | curve | Ethereum | AMM | Stablecoins |
| 6 | GMX | gmx | Arbitrum | Perps | Leverage |
| 7 | Raydium | raydium | Solana | AMM | Solana AMM |
| 8 | Jupiter | jupiter | Solana | Aggregator | Solana aggregator |
| 9 | 1inch | 1inch | Multi | Aggregator | DEX aggregator |
| 10 | SushiSwap | sushiswap | Multi | AMM | Multi-chain |

---

## TIER 5 - КОМАНДЫ И ПЕРСОНЫ (Team/People)

### Данные о командах берутся из:
| Source | Тип | Описание |
|---|---|---|
| RootData | Parser | Team members, founders |
| CryptoRank | Parser | Project teams |
| LinkedIn | Parser | Professional profiles |
| Twitter/X | Parser | Social presence |
| GitHub | API Public | Developer activity |
| Crunchbase | Parser | Company profiles |

### В Knowledge Graph уже есть:
- 73 персоны (founders, partners)
- 21 VC фонд с командами
- 186 investment relations

---

## ПОЛНЫЙ СПИСОК ПАРСЕРОВ

```
/app/backend/modules/parsers/
├── parser_activities.py      # General activities parser
├── parser_airdropalert.py    # AirdropAlert web parser
├── parser_coingecko.py       # CoinGecko API (needs key)
├── parser_coinmarketcap.py   # CMC API (needs key)
├── parser_crunchbase.py      # Crunchbase web parser
├── parser_cryptorank.py      # CryptoRank parser + API
├── parser_dappradar.py       # DappRadar parser
├── parser_defillama.py       # DefiLlama free API
├── parser_icodrops.py        # ICO Drops web parser
├── parser_incrypted.py       # Incrypted RSS parser
├── parser_messari.py         # Messari API (needs key)
├── parser_news.py            # Universal RSS parser
├── parser_rootdata.py        # RootData parser
├── parser_tokenunlocks.py    # TokenUnlocks parser
```

---

## ИТОГОВАЯ СТАТИСТИКА

| Tier | Количество | Описание |
|---|---|---|
| Tier 1 | 15 | Критически важные, всегда работают |
| Tier 2 | 17 | Важные, парсер/публичный API |
| Tier 3 | 4 | Опциональные, требуют API ключ |
| Tier 4 | 24 | Биржи (14 CEX + 10 DEX) |
| Tier 5 | 6 | Источники данных о командах |
| **Всего** | **66** | Источников данных |

### News Sources (отдельно)
- Tier A: 15 источников
- Tier B: 35 источников
- Tier C: 40 источников
- Tier D: 30 источников
- **Всего: 120** новостных источников

---

## РЕКОМЕНДАЦИИ ПО BOOTSTRAP

```python
# Порядок инициализации в bootstrap.py:
1. Seed exchanges (CEX + DEX)
2. Seed news_sources (120 RSS)
3. Seed data_sources (34 с правильными tier)
4. Build Knowledge Graph (funds, persons, projects)
5. Bootstrap entity aliases
6. Run health check (не блокирует работу)
```

**Ключевой принцип**: Система ВСЕГДА работает через парсеры. API ключи - опциональное расширение.
