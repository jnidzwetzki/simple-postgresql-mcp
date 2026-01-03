from mcp.server.fastmcp import FastMCP
import subprocess

# Initialize the MCP server
mcp = FastMCP("Local PostgreSQL database manager", json_response=True)

@mcp.tool()
def create_db(database: str) -> str:
    """Create a new local PostgresSQL database"""
    try:
        subprocess.check_output(
            ["createdb", database],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10,
        )
        return f"Database '{database}' created successfully."
    except subprocess.CalledProcessError as e:
        return f"Error creating database: {e.output.strip()}"
    except Exception as e:
        return f"Error creating database: {str(e)}"

@mcp.tool()
def drop_db(database: str) -> str:
    """Drop a PostgresSQL database"""
    try:
        subprocess.check_output(
            ["dropdb", database],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10,
        )
        return f"Database '{database}' dropped successfully."
    except subprocess.CalledProcessError as e:
        return f"Error dropping database: {e.output.strip()}"
    except Exception as e:
        return f"Error dropping database: {str(e)}"

#@mcp.resource("postgres://localhost/databases")
@mcp.tool()
def list_databases() -> str:
    """List all locally existing Postgres databases"""
    try:
        out = subprocess.check_output(
            ["psql", "postgres", "-At", "-c", "SELECT datname FROM pg_database;"],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10,
        )
        databases = [line for line in out.splitlines() if line.strip()]
        return "\n".join(databases) if databases else "No databases found."
    except subprocess.CalledProcessError as e:
        return f"Error listing databases: {e.output.strip()}"
    except Exception as e:
        return f"Error listing databases: {str(e)}"


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")