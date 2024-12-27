#!/bin/bash

# Start the Cloudflare Warp service in the background
warp-svc &

# Wait for Warp to initialize (optional, you can increase the sleep duration if needed)
sleep 5

# Run Warp CLI commands to register and connect
warp-cli --accept-tos registration new
warp-cli --accept-tos mode warp
warp-cli --accept-tos connect
warp-cli --accept-tos status

# Finally, run the main application (this will be the Python app or any command you want)
exec "$@"
