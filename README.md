# Madrid Tourist Rental Investment Analysis
> Analysis based on Madrid Airbnb listing data collected in June 2026.
## Project Overview

Management has decided to invest in Madrid and has commissioned an analysis of publicly available data from Airbnb, one of the leading platforms in the short-term rental market.

The objective is to identify the property profiles with the highest commercial potential for tourist rentals and the areas of Madrid where these opportunities are concentrated.

The analysis combines rental market performance data with estimated acquisition costs and location-based indicators to support the property sourcing strategy.

---

## Business Objective

**Identify the property profile or profiles that maximise commercial potential in Madrid's tourist rental market and the main areas where these opportunities are concentrated.**

Three factors were identified as the main profitability drivers:

* **Nightly price:** higher prices increase potential rental income.
* **Occupancy:** more occupied days increase annual revenue.
* **Acquisition price:** lower purchase prices improve investment potential.

---

## KPIs

The analysis evaluates properties using:

* **Estimated annual occupancy:** expected occupied days per year.
* **Nightly price (€):** Airbnb listed price per night.
* **Estimated acquisition price:** estimated size × average district price per m², applying a **25% negotiation discount**.
* **Estimated annual gross revenue:** calculated from nightly price and expected occupancy.
* **Gross margin:** yearly revenue expected without considering financial costs & taxes.

The metrics do not represent a complete financial model including operating costs, taxes or financing.

---

## Data & Storage

The project combines three main data sources:

* **Airbnb listings:** 2026 Madrid listing-level data from [Inside Airbnb](https://insideairbnb.com/get-the-data/?utm_source=chatgpt.com).
* **Residential prices:** average district price per m² from Idealista market data (`preciom2_madrid_2025.csv`).
* **Tourist points of interest:** coordinates of 45 major attractions (`poi_madrid.csv`).

Data was centralised using **SQLite (`sqlite3`)** in `mercado_inmobiliario.db`.

---

## Data Preparation & Feature Engineering

The dataset was prepared to create a reliable reference sample and generate variables required for the investment analysis.

### Data Quality Filters

The following records were excluded:

* Listings with less than **10 months of history**, improving the reliability of occupancy estimates.
* Nightly prices outside the **€20–€1,000** range.
* Listings with occupancy below the **25th percentile**, as the analysis focuses on commercially stronger reference properties.
* Extreme values above the **99th percentile** for `beds`, `bedrooms` and `bathrooms`, with an additional maximum of **12 beds**.

Missing values in `beds`, `bedrooms` and `bathrooms` were imputed using properties with the same `accommodates` capacity, applying the **mode when it represented at least 50% of observations and the median otherwise**.

### New Analytical Variables

Several variables required for the analysis were not available in the original data:

* **Estimated property size:** a proxy derived from available property characteristics, used to approximate acquisition cost.
* **Estimated annual gross revenue:** calculated from nightly price and occupancy, with usage adjustments for specific private and shared room configurations to avoid overestimating potential revenue.
* **Tourist Attractiveness Score (0–100):** generated from the distance to 45 major points of interest using the Haversine formula and exponential distance decay.

The tourist score function is available in `src/preprocessing.py` as `tourist_score_0_100`.

---

## Repository Structure

```text
├── data/
│   ├── raw/
│   │   └── mercado_inmobiliario.db
│   ├── intermediate/
│   └── processed/
│
├── notebooks/
├── reports/
│   ├── graphics/
│   └── maps/
├── src/
└── README.md
```

## Exploratory Data Analysis Findings

### General Gross Margin Analysis (overview)

The analysis shows that the strongest investment opportunities are concentrated around **Entire home/apt properties**, particularly those with **2 bedrooms and capacity for 4+ guests**.

At district level, the best opportunities depend on the balance between gross margin, tourism attractiveness and acquisition cost:

* **Centro** offers the strongest and most reliable combination of gross margin and tourism attractiveness.
* **Arganzuela** and **Puente de Vallecas** show the highest gross margin potential, although Puente de Vallecas has a smaller reference sample.
* **Carabanchel** offers a strong balance between gross margin, tourism attractiveness and low acquisition cost.
* **Barajas** and **Villa de Vallecas** show high gross margin potential but low tourist attractiveness, making them less suitable when tourism demand is a key investment requirement.

### Top Investment Districts

The six districts with the best overall combination of **gross margin, tourist attractiveness, occupancy and acquisition cost** were selected for deeper analysis.

| District               | Best Performing Configurations                | Median acquisition cost |
| ---------------------- | --------------------------------------------- | ----------------------: |
| **Centro**             | Entire home/apt · 4+ guests · 2 bedrooms      |               ~€283,725 |
| **Arganzuela**         | Entire home/apt · 3–4+ guests · 2 bedrooms    |               ~€237,525 |
| **Puente de Vallecas** | Entire home/apt · 3–4+ guests · 2–4+ bedrooms |               ~€124,687 |
| **Carabanchel**        | Entire home/apt · 3–4+ guests · 2 bedrooms    |               ~€139,425 |
| **Barajas**            | Entire home/apt / Private room                |               ~€183,787 |
| **Villa de Vallecas**  | Entire home/apt · 3–4+ guests · 2 bedrooms    |               ~€139,387 |

**Puente de Vallecas** stands out for its combination of tourism potential and acquisition cost, while **Centro** provides the most robust evidence due to its much larger sample.

### Gross Margin Potential with best performing configurations

Among the selected districts:

* **Puente de Vallecas:** P75 gross margin of **17.59%**.
* **Arganzuela:** P75 of **16.14%**.
* **Centro:** P90 of **17.97%**, supported by **994 reference properties**.
* **Carabanchel:** strong balance between margin and sample size, with **77 properties**.
* **Puente de Vallecas:** results should be interpreted cautiously due to its smaller sample of **22 properties**.

Barajas and Villa de Vallecas combine attractive performance metrics with low tourist attractiveness and limited samples, so they are not recommended when tourism appeal is a mandatory investment criterion.

![Gross margin by top districts](reports/graphics/gross_margin_top_districts.png)

---

### Occupancy Analysis

A second analysis evaluates opportunities from a **lower-risk perspective**, focusing on properties capable of maintaining relatively high annual occupancy.

The strongest combination of **occupancy and gross margin** is found in **Centro, Puente de Vallecas and Carabanchel**.

Other districts such as **Barajas, Villa de Vallecas and Arganzuela** also show high occupancy, while **Retiro and Moratalaz** provide comparatively stable occupancy but lower gross margin potential.

The occupancy data has a maximum of **255 days**, reflecting the upper limit present in Airbnb's estimated occupancy variable.

![Occupancy by district](reports/graphics/occupancy_by_district.png)

---

### Neighbourhood Opportunities

**Puente de Vallecas and Carabanchel** were selected for a more granular neighbourhood analysis because they combine **low acquisition costs with attractive tourism potential**.

![Neighbourhood Investment Opportunities](reports/graphics/neighbourhood_investment_opportunities.png)

The analysis identifies:

* **Best overall opportunities:** Numancia, San Diego and San Isidro.
* **Lowest acquisition cost:** Numancia, Palomeras Bajas, Portazgo, Entrevías and San Diego.
* **Highest tourist attractiveness:** Comillas, San Isidro and Opañel.

For an investment strategy prioritising **tourism potential and low acquisition cost**, **Numancia, San Diego and San Isidro** offer the strongest combination.

If acquisition cost is less restrictive, **Comillas, San Isidro and Opañel** become more attractive alternatives.

---

### High-Performing Property Configurations

A configuration-level ranking was created to identify specific combinations of neighbourhood, room type and property characteristics.

A minimum of **5 properties per configuration** was required to reduce the impact of highly unstable small samples.

The top configurations by gross margin were:

| Neighbourhood     | Property profile                                 | Gross margin | Properties |
| ----------------- | ------------------------------------------------ | -----------: | ---------: |
| **Comillas**      | Entire home/apt · 1 bedroom · 4 guests · 2 beds  |   **15.00%** |          8 |
| **Numancia**      | Entire home/apt · 1 bedroom · 3 guests · 2 beds  |   **14.65%** |          7 |
| **Puerta Bonita** | Entire home/apt · 1 bedroom · 4 guests · 2 beds  |   **14.53%** |          6 |
| **Vista Alegre**  | Entire home/apt · 1 bedroom · 4 guests · 2 beds  |   **12.36%** |          6 |
| **San Diego**     | Entire home/apt · 2 bedrooms · 4 guests · 2 beds |   **11.63%** |         11 |

The results reinforce the broader analysis: **Entire home/apt** is present in **18 of the top 20 configurations**, with **1-bedroom properties accommodating around 4 guests** appearing particularly frequently.

Because individual configurations have smaller samples, these results should be considered **supporting evidence rather than standalone investment recommendations**.

---

### Interactive Maps

The interactive versions of the geographic analysis are available in the `reports/maps/` directory:

- [Madrid Gross Margin Heatmap](reports/maps/madrid_gross_margin_heatmap.html)
- [High-Occupancy Gross Margin Heatmap](reports/maps/madrid_occupancy_heatmap.html)
- [Puente de Vallecas & Carabanchel Heatmap](reports/maps/puente_vallecas_carabanchel_heatmap.html)

### Maps & Decision Tool

Three heatmaps were created to provide a geographic view of the results:

* Overall **gross margin potential across Madrid**.
* Gross margin potential for properties with **occupancy at or above the median**.
* Detailed gross margin distribution across **Puente de Vallecas and Carabanchel**.

A prototype **custom gross margin calculator** is also available in `src/preprocessing.py`. It estimates the potential gross margin for a specific property configuration.

The calculator is an **academic prototype** rather than a production investment tool. A real-world implementation would require additional business inputs and validation from the valuation and investment teams.

---

## Recommendations

Based on the combination of gross margin, estimated occupancy, acquisition cost, tourist attractiveness and sample size, the analysis suggests the following investment priorities:

1. **Prioritise Entire home/apt properties** with approximately **1–2 bedrooms and capacity for 4+ guests**, as these profiles consistently appear among the strongest-performing configurations.

2. **Focus the initial search on Puente de Vallecas and Carabanchel** when acquisition cost is a key constraint. These districts combine relatively low estimated acquisition costs with attractive gross margin and tourism potential.

3. **Consider Centro for lower analytical risk.** Its larger reference sample provides stronger evidence for the identified property profiles, despite its higher acquisition cost.

4. **Prioritise Numancia, San Diego and San Isidro** when looking for neighbourhoods that balance tourism attractiveness and acquisition cost.


5. **Treat small-sample opportunities as candidates for further validation**, rather than direct investment recommendations. Property-level due diligence and local market validation would be required before acquisition.

---

## Future Work

The current analysis provides a screening framework rather than a complete real-estate investment model. Future work could extend it by:

* Incorporating **operating expenses, taxes, maintenance, management fees and financing** to estimate net cash flow and a more complete investment return.
* Improving the **property-size and acquisition-cost estimates** using actual property-level market data.
* Adding **time-series analysis** to evaluate seasonal demand and changes in rental performance.
* Incorporating **regulatory and licensing constraints** affecting tourist rentals in Madrid.
* Validating the most promising configurations against **additional data sources**, such as real-estate listings and transaction data.
* Developing the **gross margin calculator into an interactive decision-support tool** with additional investment parameters.


## Conclusions

The analysis points towards a clear investment profile:

> **Entire home/apt properties, generally around 1–2 bedrooms and 4+ guest capacity, located in districts combining reasonable tourist attractiveness with low acquisition costs.**

Among the analysed areas, **Centro** provides the strongest evidence and tourism profile, while **Puente de Vallecas and Carabanchel** offer particularly attractive opportunities from a **cost-to-potential perspective**.

At neighbourhood level, **Numancia, San Diego and San Isidro** emerge as the most attractive candidates when balancing acquisition cost and tourism potential.

The results also show that **gross margin alone is not sufficient to select an investment area**. Combining gross margin with occupancy, tourist attractiveness, acquisition cost and sample size produces a more robust framework for identifying potential investment opportunities.

