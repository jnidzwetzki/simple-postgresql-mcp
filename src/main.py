from mcp.server.fastmcp import FastMCP
import subprocess

# Initialize the MCP server
mcp = FastMCP("PostgreSQL MCP Server", json_response=True)

@mcp.tool()
def create_db(database: str) -> str:
    """Create a new local PostgreSQL database"""
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
    """Drop a PostgreSQL database"""
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

@mcp.tool()
def list_databases() -> str:
    """List all locally existing PostgreSQL databases"""
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

@mcp.tool()
def execute_sql(database: str, sql: str, timeout: int = 30) -> str:
    """Execute a SQL statement on the given local PostgreSQL database.

    Returns command output on success or the error output on failure.
    """
    try:
        out = subprocess.check_output(
            ["psql", database, "-v", "ON_ERROR_STOP=1", "-c", sql],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return out.strip() if out.strip() else "Command executed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error executing SQL: {e.output.strip()}"
    except Exception as e:
        return f"Error executing SQL: {str(e)}"

# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
