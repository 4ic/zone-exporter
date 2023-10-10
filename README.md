# zone-exporter

## Overview

The `zone-exporter` Python script processes CSV files containing postcodes, suburbs, and shipping prices. It then generates plain text files that group price tiers together. The script categorises the shipping zones into three categories: General, Variable, and Excluded. 

- **General zones**: Suburbs with unique names.
- **Variable zones**: Suburbs with non-unique names and unique postcodes.
- **Excluded zones**: Suburbs with a shipping price greater than $200.

For each category, the script generates separate plain text files. These files are saved in a folder named after the input CSV file within the `export` directory.

## Input

Place the input CSV files in the `import` folder. These files should have the following columns:

- `Postcode`: The postcode of the suburb.
- `Suburb`: The name of the suburb.
- `Customer price`: The shipping price for the suburb.

Example input `bike-zones.csv` file:

```
Postcode,Suburb,Customer price
3193,BEAUMARIS,29.99
3549,HAPPY VALLEY,59.99
4300,SPRINGFIELD,39.99
...
```

## Output

For each input CSV file, the script generates the following plain text files in a subfolder within the `export` directory:

- `general.txt`: List of suburb names for each General zone with different prices. Separated by `|`.
- `variable-suburb.txt`: List of suburb names for each Variable zone with different prices. Separated by `|`.
- `variable-postcode.txt`: List of postcodes for each Variable zone with different prices. Separated by `|`.
- `excluded.txt`: List of suburb names and postcodes for all Excluded zones in plain text.

Example output files:

`29-general.txt`:

```
WILLOUGHBY EAST|CASTLE COVE|ROSEVILLE...
```

`139-variable-suburb.txt`:

```
BLACK MOUNTAIN|SANDILANDS|THERESA CREEK|BELL|WELLESLEY...
```

`139-variable-postcode.txt`:

```
2365|2469|2469...
```

`Excluded.txt`:

```
FREEBURN ISLAND (2464), GOAT ISLAND (2477), PIMLICO ISLAND (2478)...
```

A `log.txt` file is generated in each subfolder within the `export` directory. This log contains the count of suburbs in each General and Variable zone (sorted by price) and the count of suburbs in the Excluded zone.

Example `log.txt` file:

```
59.99 General zone: 35
89.99 Variable zone: 10
199.99 General zone: 4
...
Excluded zone: 50
```

## Usage

The generated text files are formatted for use with Parcelify, a Shopify app. For app details, visit [Parcelify on Shopify](https://apps.shopify.com/parcelify). Users can directly copy the contents into Parcelify to configure shipping rates. Two rates are created for each price tier, the first rate is based solely on matching the suburb name. While the second rate uses both the suburb name and postcode for matching.

## Notes

- The script determines the zone type (General or Variable) based on the uniqueness of the suburb names. A suburb name that appears only once is considered a General zone, while names appearing multiple times are considered Variable zones.
- Suburbs with shipping prices greater than $200 are automatically categorised as Excluded zones, this value is chosen based on the businesses individual tolerance to risk.
- The script can process multiple import files, such as adult bikes, eBikes, and kid bikes.
