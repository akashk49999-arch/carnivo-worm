**demo.sh:**
```bash
#!/bin/bash
echo "=== Simple Worm Pentest Demo ==="
echo "1. Start C2 listener: nc -lvnp 4444"
echo "2. Deploy: python3 worm.py --demo"
echo "3. Observe propagation in lab environment"