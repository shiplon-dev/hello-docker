# hello-docker

Test app for Shiplon's **Dockerfile** runtime: a tiny Python server, to show the
app does not have to be Node.js. Shiplon builds this repository's own Dockerfile.

| Shiplon setting | Value |
|---|---|
| Runtime | Dockerfile |
| Port | `8080` |
| Health check path | `/healthz` |

Optional environment variable: `APP_MESSAGE` (shown on the page).

Rules for any Dockerfile on Shiplon:
- Listen on `0.0.0.0` and on the port set in Shiplon (it is also passed as `PORT`).
- Run as a numeric non-root user (`USER 10001`). Images that run as root, or set a
  user by name, are refused by the cluster.
- Memory limit is 512 MB per app container; builds get up to 3 GB.

Run locally: `docker build -t hello-docker . && docker run --rm -p 8080:8080 hello-docker`
