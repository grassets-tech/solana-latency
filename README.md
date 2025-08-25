# Solana-latency

Current script checks the latency to the solana valiadators from current node.

> NOTE: This is light script, with preconfigured in/out file names.

## How to use

 - Get the solana validators IP addresses from the gossip or any other sources
 - Store in the scv file with name `ips.csv`
 - Run python script `ping_test_bulk.py`

```
python3 ping_test_bulk.py
```
 - Check the output in the generated file `ping_results.csv`


