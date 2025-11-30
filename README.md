# Vexen-User

Sistema de gestión de usuarios con arquitectura hexagonal, diseñado para integrarse con vexen-rbac y vexen-auth.

## Características

- **Arquitectura Hexagonal**: Separación clara entre dominio, aplicación e infraestructura
- **Async/Await**: Totalmente asíncrono usando SQLAlchemy 2.0+ con asyncpg
- **Type Safe**: Completamente tipado para mejor soporte en IDEs
- **API Pública Simple**: Similar a FastAPI, fácil de usar
- **Paginación y Filtros**: Soporte completo para búsqueda, filtros y paginación
- **Estadísticas**: Obtén métricas sobre usuarios del sistema

## Implementado

✅ **Entidades**: User entity completa con validaciones
✅ **Repositorios**: IUserRepositoryPort (interface) e implementación SQLAlchemy
✅ **DTOs**: Todas las estructuras de request/response según especificaciones
✅ **Casos de Uso**: list, get, create, update, delete, stats
✅ **Servicio**: UserService que orquesta los casos de uso
✅ **API Pública**: VexenUser class (similar a RBAC)
✅ **Adapters**: Gestión de sesiones SQLAlchemy
✅ **Ejemplo funcional**: example_usage.py

## Uso Rápido

```python
import asyncio
from vexen_user import VexenUser
from vexen_user.application.dto import CreateUserRequest

async def main():
    user_system = VexenUser(
        database_url="postgresql+asyncpg://user:pass@localhost/db"
    )

    await user_system.init()

    # Crear usuario
    user = await user_system.service.create(
        CreateUserRequest(
            email="user@example.com",
            name="John Doe"
        )
    )

    # Listar usuarios
    users = await user_system.service.list(page=1, page_size=20)

    # Obtener estadísticas
    stats = await user_system.service.stats()

    await user_system.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Instalación

```bash
pip install vexen-user
```

## Estructura del Proyecto

```
vexen_user/
├── domain/              # Capa de dominio (entidades, puertos)
│   ├── entity/         # User entity
│   └── repository/     # IUserRepositoryPort
├── application/        # Capa de aplicación (casos de uso, DTOs)
│   ├── dto/           # Request/Response DTOs
│   ├── usecase/       # Casos de uso
│   └── service/       # UserService
└── infraestructure/   # Capa de infraestructura (adaptadores)
    └── output/
        └── persistence/
            └── sqlalchemy/  # SQLAlchemy adapter
```

## DTOs Disponibles

### Request DTOs
- `CreateUserRequest`: Crear nuevo usuario
- `UpdateUserRequest`: Actualizar usuario completo
- `PatchUserRequest`: Actualizar campos específicos

### Response DTOs
- `UserResponse`: Información básica de usuario
- `UserExpandedResponse`: Información completa con metadatos
- `PaginatedUsersResponse`: Lista paginada de usuarios
- `UserStatsResponse`: Estadísticas del sistema

## Casos de Uso

- `ListUsers`: Listar usuarios con paginación y filtros
- `GetUser`: Obtener usuario por ID o email
- `CreateUser`: Crear nuevo usuario
- `UpdateUser`: Actualizar usuario
- `DeleteUser`: Eliminar usuario (soft delete)
- `GetUserStats`: Obtener estadísticas

## Integración con otros sistemas

Este paquete está diseñado para trabajar con:
- `vexen-rbac`: Sistema de control de acceso basado en roles
- `vexen-auth`: Sistema de autenticación

## Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar tests
pytest

# Formatear código
ruff format .

# Linting
ruff check . --fix
```

## Licencia

MIT

## Links

- [PyPI](https://pypi.org/project/vexen-user/)
- [Repositorio](https://github.com/vexen-labs/vexen-user)
- [Documentación](https://github.com/vexen-labs/vexen-user#readme)
