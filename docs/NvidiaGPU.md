{# NVIDIA Graphics Card Optimization on Ubuntu Linux

## Overview
This guide provides step-by-step instructions to optimize the usage of an NVIDIA graphics card on an Ubuntu Linux system. It covers monitoring GPU usage, addressing high utilization, and reducing power consumption and fan noise.

---

## 1. Checking GPU Status
To monitor GPU usage, use the `nvidia-smi` command:

```bash
nvidia-smi
```

### Example Output
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.120                Driver Version: 550.120        CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------|
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 2060        Off |   00000000:01:00.0  On |                  N/A |
|  0%   49C    P8             21W /  172W |     484MiB /   6144MiB |     31%      Default |
+-----------------------------------------+------------------------+----------------------+
```

### Key Observations:
- **Fan**: GPU fan status.
- **Temperature**: Current GPU temperature.
- **Power Usage**: Current and maximum power consumption.
- **Memory Usage**: Amount of GPU memory being used.
- **Processes**: Lists applications utilizing the GPU.

---

## 2. Identifying Resource-Intensive Processes
Run the following to identify processes using the GPU:

```bash
nvidia-smi
```

### Terminate Unnecessary Processes
1. Note the **PID** of the process.
2. Kill the process:
   ```bash
   sudo kill -9 <PID>
   ```

---

## 3. Adjusting Power Limits
To reduce power consumption and fan noise, set a power limit:

1. Check the valid power range from the `nvidia-smi` output.
2. Set the power limit (e.g., **125 W**):
   ```bash
   sudo nvidia-smi -pl 125
   ```
3. Verify the new power limit:
   ```bash
   nvidia-smi
   ```

### Error Handling
If you receive an error like:
```
Provided power limit 100.00 W is not a valid power limit which should be between 125.00 W and 172.50 W for GPU 00000000:01:00.0
```
Use a value within the valid range.

---

## 4. Reducing GNOME Desktop Environment Usage
GNOME's animations and graphical features can increase GPU load. To reduce this:

### Disable Animations
```bash
gsettings set org.gnome.desktop.interface enable-animations false
```

### Switch to a Lightweight Desktop Environment
Install and switch to a lighter environment like XFCE:

```bash
sudo apt install xfce4
```

---

## 5. Updating NVIDIA Drivers
Ensure you have the latest NVIDIA driver installed:

```bash
sudo apt update
sudo apt install nvidia-driver-535
```
Replace `535` with the recommended driver version for your GPU.

---

## 6. Monitoring GPU After Changes
After applying the optimizations, monitor GPU usage again:

```bash
nvidia-smi
```

---

## 7. Adjusting Fan Curves (Optional)
To manually control the fan speed:

1. Open NVIDIA settings:
   ```bash
   nvidia-settings
   ```
2. Navigate to **Thermal Settings** and adjust the fan curve.

---

## Summary
By following this guide, you can:
- Monitor and manage GPU usage.
- Reduce unnecessary power consumption.
- Optimize desktop environment settings.
- Ensure the GPU operates within an acceptable temperature and noise level.

For further assistance, consult NVIDIA's official documentation or Ubuntu forums.
