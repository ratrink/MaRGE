# Findings from 26.11.2024

## Summary of the Tests

During the gradient tests, we noticed that they immediately pushed the gradient amplifier to its limits, resulting in a significant offset. Despite various shimming sequences and manual shimming, it was not possible to fully resolve this issue.

Further tests revealed that the DACs activate an offset when the amplifiers are turned on.

## Changes in `grad_board.py`

The configuration of the DAC values is handled in the file `mercos_client/grad_board.py`, starting from line 105. It turned out to be beneficial to change the order of the commands:
- **Before:** Turn on the amplifiers first, then set the outputs to 0.  
- **After:** Set the outputs to 0 first, then turn on the amplifiers.  

We swapped line 110 with line 109 to implement this adjustment.  

The commands are written in hexadecimal and address the individual registers of the DACs. For more details, see the DAC datasheet ([Datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/AD5781.pdf), from page 19).

The offset only appears with the final command (`0x07200002`); prior to this, the system is perfectly set to 0. However, if this command is omitted, gradients cannot be generated using either `examples.py` or `MaRGE`.  

By manually adjusting the offset (e.g., setting it to 200 instead of 0 → `0x04100200`), we observed improvements. However, the offset reappeared as soon as a gradient was activated.

## Hardware Adjustment: Voltage Divider

To reduce the offset, we introduced a 10:1 voltage divider. At the same time, we adjusted the gradient amplification (`gFactor`) in the MaRGE configuration file (`hw_config.py`) by a factor of 10 to maintain previous results.  
- Example:  
  - **Before:** `gFactor` = 0.05  
  - **After:** `gFactor` = 0.005  
  - Similar adjustments were made for other values (e.g., 0.035 → 0.0035).

## Final Configuration File

The configuration file (`hw_config.py`) now looks as follows:  
[hw_config.py](./hw_config.py)
