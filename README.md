# 📊 Veterinary Analytics API

Backend analítico para una plataforma de veterinarias usando **FastAPI + Supabase (PostgreSQL)**.
Este servicio expone endpoints de analítica listos para ser consumidos por **Power BI**, **dashboards web** o un **frontend (React / Next.js)**.

---

## 1️⃣ Crear y activar el entorno virtual

### Crear entorno virtual

```bash
python -m venv venv
```

venv\Scripts\activate


## 2️⃣ Instalación de dependencias

Instalar los paquetes necesarios:

pip install -r requirements.txt


## 4️⃣ Variables de entorno (`.env`)

Crear el archivo `.env` en la raíz del proyecto.

Aquí se guardan **credenciales sensibles** y  **configuración de Supabase** .

`<pre class="overflow-visible! px-0!" data-start="1398" data-end="1711"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary">``<div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2">``<div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div>``</div></div>``<div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-env">``<span>`# PostgreSQL Supabase
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432
DB_USER=postgres.<project_ref>
DB_PASSWORD=TU_PASSWORD
DB_NAME=postgres
DB_SSL=true `</code></div>``</div></pre>`

## 5️⃣ Estructura del proyecto

<pre class="overflow-visible! px-0!" data-start="1793" data-end="1988"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-text"><span><span>Analitica-x/
│
├── main.py
├── database.py
├── test_connection.py
├── .env
├── requirements.txt
│
├── routers/
│   ├── admin_analytics.py
│   └── veterinarian_analytics.py
│
└── venv/
</span></span></code></div></div></pre>

---

## 6️⃣ Conexión a base de datos (`database.py`)

Archivo encargado de crear la conexión con PostgreSQL (Supabase).

<pre class="overflow-visible! px-0!" data-start="2111" data-end="2665"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>import</span><span> psycopg2
</span><span>import</span><span> os
</span><span>from</span><span> dotenv </span><span>import</span><span> load_dotenv

load_dotenv()

</span><span>def</span><span></span><span>get_db_connection</span><span>():
    </span><span>try</span><span>:
        conn = psycopg2.connect(
            host=os.getenv(</span><span>"DB_HOST"</span><span>),
            port=os.getenv(</span><span>"DB_PORT"</span><span>),
            user=os.getenv(</span><span>"DB_USER"</span><span>),
            password=os.getenv(</span><span>"DB_PASSWORD"</span><span>),
            dbname=os.getenv(</span><span>"DB_NAME"</span><span>),
            sslmode=</span><span>"require"</span><span></span><span>if</span><span> os.getenv(</span><span>"DB_SSL"</span><span>) == </span><span>"true"</span><span></span><span>else</span><span></span><span>"disable"</span><span>
        )
        </span><span>return</span><span> conn
    </span><span>except</span><span> Exception </span><span>as</span><span> e:
        </span><span>print</span><span>(</span><span>"DB connection error:"</span><span>, e)
        </span><span>return</span><span></span><span>None</span><span>
</span></span></code></div></div></pre>

---

## 7️⃣ Prueba de conexión (`test_connection.py`)

Archivo para validar que la conexión con Supabase funciona correctamente.

<pre class="overflow-visible! px-0!" data-start="2797" data-end="3074"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> database </span><span>import</span><span> get_db_connection

conn = get_db_connection()

</span><span>if</span><span> conn:
    cur = conn.cursor()
    cur.execute(</span><span>"SELECT version();"</span><span>)
    </span><span>print</span><span>(</span><span>"Conexión exitosa"</span><span>)
    </span><span>print</span><span>(cur.fetchone())
    cur.close()
    conn.close()
</span><span>else</span><span>:
    </span><span>print</span><span>(</span><span>"Error de conexión"</span><span>)
</span></span></code></div></div></pre>

Ejecutar:

<pre class="overflow-visible! px-0!" data-start="3086" data-end="3123"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python test_connection.py
</span></span></code></div></div></pre>

---

## 8️⃣ Endpoints de analítica administrativa (`routers/admin_analytics.py`)

Endpoints globales para administradores.

* Clínicas con más servicios
* Animales más atendidos
* Clientes por mes

<pre class="overflow-visible! px-0!" data-start="3323" data-end="3488"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> fastapi </span><span>import</span><span> APIRouter
</span><span>from</span><span> database </span><span>import</span><span> get_db_connection

router = APIRouter(
    prefix=</span><span>"/admin/analytics"</span><span>,
    tags=[</span><span>"Admin Analytics"</span><span>]
)
</span></span></code></div></div></pre>

(Los endpoints devuelven datos listos para gráficos).

---

## 9️⃣ Endpoints de analítica veterinaria (`routers/veterinarian_analytics.py`)

Endpoints filtrados por clínica.

* Servicios más solicitados
* Clientes frecuentes
* Servicios por período (año / mes / día)

<pre class="overflow-visible! px-0!" data-start="3758" data-end="3944"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> fastapi </span><span>import</span><span> APIRouter, Query
</span><span>from</span><span> database </span><span>import</span><span> get_db_connection

router = APIRouter(
    prefix=</span><span>"/veterinarian/analytics"</span><span>,
    tags=[</span><span>"Veterinarian Analytics"</span><span>]
)
</span></span></code></div></div></pre>

---

## 🔟 Archivo principal (`main.py`)

Inicializa la API y registra todos los routers.

<pre class="overflow-visible! px-0!" data-start="4037" data-end="5079"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> fastapi </span><span>import</span><span> FastAPI
</span><span>from</span><span> database </span><span>import</span><span> get_db_connection
</span><span>from</span><span> routers.admin_analytics </span><span>import</span><span> router </span><span>as</span><span> admin_analytics_router
</span><span>from</span><span> routers.veterinarian_analytics </span><span>import</span><span> router </span><span>as</span><span> veterinarian_analytics_router

app = FastAPI(
    title=</span><span>"Veterinary Analytics API"</span><span>,
    version=</span><span>"1.0.0"</span><span>
)

</span><span>@app.get("/"</span><span>)
</span><span>def</span><span></span><span>root</span><span>():
    </span><span>return</span><span> {
        </span><span>"message"</span><span>: </span><span>"API activa"</span><span>,
        </span><span>"endpoints"</span><span>: [
            </span><span>"/health/db"</span><span>,
            </span><span>"/admin/analytics/*"</span><span>,
            </span><span>"/veterinarian/analytics/*"</span><span>
        ]
    }

</span><span>@app.get("/health/db"</span><span>)
</span><span>def</span><span></span><span>check_db</span><span>():
    conn = get_db_connection()
    </span><span>if</span><span></span><span>not</span><span> conn:
        </span><span>return</span><span> {</span><span>"status"</span><span>: </span><span>"error"</span><span>}

    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchone()[</span><span>0</span><span>]
    cur.close()
    conn.close()

    </span><span>return</span><span> {
        </span><span>"status"</span><span>: </span><span>"ok"</span><span>,
        </span><span>"tables_in_public_schema"</span><span>: tables
    }

app.include_router(admin_analytics_router)
app.include_router(veterinarian_analytics_router)
</span></span></code></div></div></pre>

---

## 1️⃣1️⃣ Ejecutar la API

Con el entorno virtual activo:

<pre class="overflow-visible! px-0!" data-start="5145" data-end="5182"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>uvicorn main:app --reload</span></span></code></div></div></pre>
