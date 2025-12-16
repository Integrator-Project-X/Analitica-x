
# 📊 Veterinary Analytics API

Analytical backend for a veterinary platform built with  **FastAPI + Supabase (PostgreSQL)** .

This service exposes analytics endpoints ready to be consumed by  **Power BI** ,  **web dashboards** , or a  **frontend (React / Next.js)** .

---

## 1️⃣ Create and activate the virtual environment

### Create virtual environment

<pre class="overflow-visible! px-0!" data-start="477" data-end="508"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m venv venv
</span></span></code></div></div></pre>

### Activate it (Windows)

<pre class="overflow-visible! px-0!" data-start="537" data-end="570"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>venv\Scripts\activate
</span></span></code></div></div></pre>

---

## 2️⃣ Install dependencies

Install the required packages:

<pre class="overflow-visible! px-0!" data-start="638" data-end="681"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -r requirements.txt
</span></span></code></div></div></pre>

---

## 4️⃣ Environment variables (`.env`)

Create a `.env` file at the root of the project.

This file stores **sensitive credentials** and  **Supabase configuration** .

<pre class="overflow-visible! px-0!" data-start="853" data-end="1028"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-env"><span># PostgreSQL Supabase
DB_HOST=aws-0-us-west-2.pooler.supabase.com
DB_PORT=5432
DB_USER=postgres.<project_ref>
DB_PASSWORD=YOUR_PASSWORD
DB_NAME=postgres
DB_SSL=true
</span></code></div></div></pre>

---

## 5️⃣ Project structure

<pre class="overflow-visible! px-0!" data-start="1061" data-end="1256"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-text"><span><span>Analitica-x/
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

## 6️⃣ Database connection (`database.py`)

This file is responsible for creating the PostgreSQL (Supabase) connection.

<pre class="overflow-visible! px-0!" data-start="1384" data-end="1938"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>import</span><span> psycopg2
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

## 7️⃣ Connection test (`test_connection.py`)

Used to validate that the Supabase connection works correctly.

<pre class="overflow-visible! px-0!" data-start="2056" data-end="2337"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> database </span><span>import</span><span> get_db_connection

conn = get_db_connection()

</span><span>if</span><span> conn:
    cur = conn.cursor()
    cur.execute(</span><span>"SELECT version();"</span><span>)
    </span><span>print</span><span>(</span><span>"Connection successful"</span><span>)
    </span><span>print</span><span>(cur.fetchone())
    cur.close()
    conn.close()
</span><span>else</span><span>:
    </span><span>print</span><span>(</span><span>"Connection error"</span><span>)
</span></span></code></div></div></pre>

Run the test:

<pre class="overflow-visible! px-0!" data-start="2354" data-end="2391"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python test_connection.py
</span></span></code></div></div></pre>

---

## 8️⃣ Administrative analytics endpoints (`routers/admin_analytics.py`)

Global analytics endpoints for administrators.

**Includes:**

* Clinics with the most services
* Most attended animal types
* Clients per month

<pre class="overflow-visible! px-0!" data-start="2617" data-end="2782"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> fastapi </span><span>import</span><span> APIRouter
</span><span>from</span><span> database </span><span>import</span><span> get_db_connection

router = APIRouter(
    prefix=</span><span>"/admin/analytics"</span><span>,
    tags=[</span><span>"Admin Analytics"</span><span>]
)
</span></span></code></div></div></pre>

*(Endpoints return data already formatted for charts.)*

---

## 9️⃣ Veterinary analytics endpoints (`routers/veterinarian_analytics.py`)

Clinic-filtered analytics endpoints.

**Includes:**

* Most requested services
* Frequent clients
* Services by period (year / month / day)

<pre class="overflow-visible! px-0!" data-start="3063" data-end="3249"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> fastapi </span><span>import</span><span> APIRouter, Query
</span><span>from</span><span> database </span><span>import</span><span> get_db_connection

router = APIRouter(
    prefix=</span><span>"/veterinarian/analytics"</span><span>,
    tags=[</span><span>"Veterinarian Analytics"</span><span>]
)
</span></span></code></div></div></pre>

---

## 🔟 Main application file (`main.py`)

Initializes the API and registers all routers.

<pre class="overflow-visible! px-0!" data-start="3345" data-end="4387"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>from</span><span> fastapi </span><span>import</span><span> FastAPI
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
        </span><span>"message"</span><span>: </span><span>"API active"</span><span>,
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

## 1️⃣1️⃣ Run the API

With the virtual environment activated:

<pre class="overflow-visible! px-0!" data-start="4458" data-end="4495"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>uvicorn main:app --reload</span></span></code></div></div></pre>
