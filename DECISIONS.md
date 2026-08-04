# Decisions

Notes and explanations for why certain tools were chosen.

## Gunicorn

Why Gunicorn?

Gunicorn is a WSGI (Web Server Gateway Interface) HTTP sever, designed for serving Pyhon web apps in production environments.

It is:

- **Efficient**
  - spawns mutltiple worker processes
    - able to handle multiple requests simultaneously
    - concurrent, ideal for high-traffic
- **Performant & Reliabile**
  - optimized for production use
  - Error management
    - able to automatically restart failing processes
- **Compatibile with frameworks**
  - has support for Django & Flask
  - configurable number of workers
- **Has integration with other servers**
  - Nginx compatibile


> [!NOTE]
> *Flask or Django by themselves are single-threaded, which may result in bottlenecks.*
