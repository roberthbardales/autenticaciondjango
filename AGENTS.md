# autenticaciondjango

Sistema de autenticación con Django, roles y panel de usuario. Orientado a una clínica/hospital con roles: Administrador, Doctor, Recepción, Paciente.

---

## Stack

| Componente | Versión |
|-----------|---------|
| Django | 3.2.25 (LTS, EOL) |
| Python | 3.10 |
| Base de datos | PostgreSQL |
| CSS | Tailwind CSS (CDN Play) |
| JS | Vanilla (sin framework) |
| Entorno | `django-environ` (.env) |

## Dependencias principales

- `Django==3.2.25`
- `django-environ==0.11.2`
- `psycopg2-binary==2.9.9`
- `Pillow==9.5.0` (sin usar aún)
- `django-model-utils==5.0.0` (sin usar aún)

## Estructura del proyecto

```
autenticaciondjango/
├── autenticaciondjango/        # Proyecto raíz
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── applications/
│   ├── home/                   # App landing page
│   │   ├── views.py            # IndexView (TemplateView)
│   │   └── urls.py             # app_name = 'app_home'
│   └── users/                  # App usuarios
│       ├── models.py           # User custom
│       ├── views.py            # Register, Login, Logout, UpdatePassword, Dashboard, ListaUsuarios
│       ├── forms.py            # UserRegisterForm, LoginForm, UpdatePasswordForm
│       ├── urls.py             # app_name = 'app_users'
│       ├── admin.py            # UserAdmin personalizado
│       ├── managers.py         # UserManager
│       ├── mixins.py           # Permisos por rol
│       └── migrations/
├── templates/
│   ├── base.html               # Layout con Tailwind
│   ├── home/index.html         # Landing page
│   ├── users/register.html     # Registro
│   ├── users/login.html        # Login
│   ├── users/dashboard.html    # Perfil
│   ├── users/cambiar_password.html
│   ├── users/lista_usuarios.html
│   └── include/header.html, footer.html
├── static/                     # Creado, vacío
├── media/                      # Creado, vacío
├── fixtures/                   # Creado, vacío
├── requirements.txt
├── .env (ignorado por git)
└── AGENTS.md
```

## Modelo User (`users.User`)

- Hereda de `AbstractBaseUser` + `PermissionsMixin`
- `USERNAME_FIELD = 'email'`
- `REQUIRED_FIELDS = ['first_name', 'last_name']`
- Campos: `email` (unique), `first_name`, `last_name`, `occupation`, `gender`, `date_birth`, `phone`, `is_staff`, `is_active`
- Usa `UserManager` (custom)

### Choices

**occupation**: `'0'` Administrador, `'1'` Paciente, `'2'` Recepción, `'3'` Doctor
**gender**: `'M'` Masculino, `'F'` Femenino, `'O'` Otro

## URLs

### `app_home` (namespace)
| URL | View | Name |
|-----|------|------|
| `/` | `IndexView` | `index` |

### `app_users` (namespace)
| URL | View | Name |
|-----|------|------|
| `/users/` | `DashboardView` | `dashboard` |
| `/users/register/` | `UserRegisterView` | `register` |
| `/users/login/` | `LoginUser` | `login` |
| `/users/logout/` | `LogoutView` | `logout` |
| `/users/update/` | `UpdatePasswordView` | `user-update` |
| `/users/lista/` | `ListaUsuariosView` | `user-list` |

## Mixins de permisos

- `AdministradorPermisoMixin` — solo `occupation == '0'`
- `DoctorPermisoMixin` — Admin o Doctor
- `RecepcionPermisoMixin` — Admin o Recepción
- `PacientePermisoMixin` — Admin o Paciente
- `login_url` → `app_users:login`

## Settings relevantes

```python
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'app_users:login'
LOGIN_REDIRECT_URL = 'app_users:dashboard'
LOGOUT_REDIRECT_URL = 'app_users:login'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
```

## Estilo y convenciones

- **CSS**: Tailwind CDN en `base.html`, estilos inline con clases utilitarias
- **Navbar**: menú responsive con vanilla JS toggle (sin Alpine.js ni jQuery)
- **Formularios**: widgets con clase `INPUT_CLASS` definida en `forms.py`
- **Encoding**: todos los textos en español, UTF-8
- **Mensajes flash**: mapeo de `message.tags` a colores Tailwind (success → verde, error → rojo, etc.)

## Pendientes / Mejoras futuras

- Migrar Django 3.2 → 4.2 LTS o 5.0 (EOL desde abril 2024)
- Remover `USE_L10N` de settings (deprecado)
- Mover Tailwind CDN a build estático con CLI para producción
- Agregar tests
- Implementar lógica de negocio en `services.py`
- Usar `Pillow` para avatar/foto de perfil
- Corregir typo `procesors` en comentario de settings

## Comandos útiles

```bash
# Activar entorno
venv\Scripts\activate

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Admin
python manage.py createsuperuser

# Estáticos
python manage.py collectstatic
```
