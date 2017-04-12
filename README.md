# marketmove

Calculate historical market moves (by points or percentages)

This script will show market moves over the input dataset based on user input
(days and percentage or days and points).

## Pre-requisites

To ensure the script runs on your system, you will need:

1. Python
2. Python CSV library (dependency for the script to run)
3. Your dataset -- you can pull this directly from finance.yahoo.com. I just
   search for the underlying (SPX in this case) and pull down the historical
   dataset in CSV. There is no need to alter the data you download, just feed it
   into the script. Or you can download the SPX dataset I have uploaded to this
   repository to run it for yourself the first time.

## Usage

The script requires you to add three (3) parameters:

1. input file - your yahoo finance downloaded data
2. days - The ranges of trading days to factor into the 'move'
3. percentage OR points - The percentage or points in your requirement


## Examples

If you wanted to know how many times SPX breached 1% move (up or down) over a 3
trading session over the dataset, then you run it as:

  `./market_move.py -i spx_042012-042017.csv -d 3 -p 1`

The script will traverse each trading day in your dataset and shift by 3 days
then compare the closing prices of that range, if it breaches your percentage
input (1% in this case), it will output the range in which it breached. Also, at
the end of the run, it will output how many breaches occurred over the entire
dataset based on your input.

For points, same except you pass in -t with your points value. For example:

  `./market_move.py -i spx_042012-042017.csv -d 3 -t 25`

## Output

http://imgur.com/a/6HXVB

## Help?

Ping me on Reddit: /u/roundqube
