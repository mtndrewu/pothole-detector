## GitHub Copilot Chat

- Extension: 0.43.0 (prod)
- VS Code: 1.115.0 (41dd792b5e652393e7787322889ed5fdc58bd75b)
- OS: linux 6.8.0-1044-azure x64
- Remote Name: codespaces
- Extension Kind: Workspace
- GitHub Account: mtndrewu

## Network

User Settings:
```json
  "http.systemCertificatesNode": true,
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 140.82.114.5 (125 ms)
- DNS ipv6 Lookup: Error (25 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (43 ms)
- Electron fetch: Unavailable
- Node.js https: HTTP 200 (124 ms)
- Node.js fetch (configured): HTTP 200 (167 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.113.22 (12 ms)
- DNS ipv6 Lookup: Error (10 ms): getaddrinfo ENOTFOUND api.individual.githubcopilot.com
- Proxy URL: None (25 ms)
- Electron fetch: Unavailable
- Node.js https: HTTP 200 (151 ms)
- Node.js fetch (configured): HTTP 200 (51 ms)

Connecting to https://proxy.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 20.85.130.105 (4 ms)
- DNS ipv6 Lookup: Error (6 ms): getaddrinfo ENOTFOUND proxy.individual.githubcopilot.com
- Proxy URL: None (20 ms)
- Electron fetch: Unavailable
- Node.js https: HTTP 200 (127 ms)
- Node.js fetch (configured): HTTP 200 (208 ms)

Connecting to https://mobile.events.data.microsoft.com: HTTP 404 (151 ms)
Connecting to https://dc.services.visualstudio.com: HTTP 404 (170 ms)
Connecting to https://copilot-telemetry.githubusercontent.com/_ping: HTTP 200 (126 ms)
Connecting to https://telemetry.individual.githubcopilot.com/_ping: HTTP 200 (115 ms)
Connecting to https://default.exp-tas.com: HTTP 400 (170 ms)

Number of system certificates: 354

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).