from aiohttp import web
import markdown
import os

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    # Correct path: project_root/README.md
    readme_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "README.md"
    )

    # If README not found → still return 200 (important for uptime)
    if not os.path.exists(readme_path):
        return web.Response(text="OK", status=200)

    with open(readme_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = markdown.markdown(
        md_text,
        extensions=["fenced_code", "codehilite", "tables"]
    )

    html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Yugen FileStore</title>
    </head>
    <body>
        {html}
    </body>
    </html>
    """

    return web.Response(text=html_page, content_type="text/html")

async def web_server():
    app = web.Application()
    app.add_routes(routes)
    return app
