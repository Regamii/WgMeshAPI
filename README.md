# WgMeshAPI
REST API for configuring WireGuard in a Mesh

## What is WgMeshAPI
**Wg** short for [WireGuard](https://www.wireguard.com/) simple modern and fast VPN. **Mesh** in networking terms is topology where every node has a connection to the other nodes in a network. This means that in a mesh network every node can contact eachother, no restrictions. Partially Connected Mesh Network has been taken into consideration, but it adds a level of complexity. **API** Application Programming Interface.

## Why WgMeshAPI
Why WgMeshAPI when there are probably better tools like k4yt3x/wg-meshconfig and costela/wesher https://github.com/search?utf8=%E2%9C%93&q=wireguard%20mesh? With an API clients can manage their own configurations. Why is this useful? With a tool like [k4yt3x/wg-meshconfig](https://github.com/k4yt3x/wg-meshconf) you install the tool locally, and configs are generated locally. When you've generated the configs the next step is to find a way to efficiently and securely give the nodes the configs. This is NOT a huge problem, but in my opinion it would be better if a client can download new configurations from a secure location.

## Security
