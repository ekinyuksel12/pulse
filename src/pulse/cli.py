import click
import asyncio
import sys
from typing import Type
from loguru import logger

from pulse.auth.manager import AuthManager
from pulse.core.base import BasePlatform
from pulse.platforms.github.processor import GitHubPlatform
from pulse.platforms.linkedin.processor import LinkedInPlatform

# Configure logger for the CLI
logger.remove()
logger.add(sys.stderr, format="<level>{message}</level>", level="INFO")

class PulseCLI(click.Group):
    """Custom CLI group to handle dynamic platform loading."""
    def list_commands(self, ctx):
        return ["auth", "github", "linkedin", "reddit"]

@click.group(cls=PulseCLI)
@click.pass_context
def main(ctx):
    """🌌 Pulse: Your Digital Identity, Extracted for the AI Era."""
    ctx.obj = AuthManager()

@main.group()
def auth():
    """Manage credentials for various platforms."""
    pass

@auth.command(name="github")
@click.option('--token', help='GitHub Personal Access Token')
@click.option('--username', help='GitHub Username')
@click.pass_obj
def auth_github(auth_manager, token, username):
    """Authenticate with GitHub."""
    if not token or not username:
        click.echo("--- GitHub Auth Guide ---")
        click.echo("1. Go to https://github.com/settings/tokens")
        click.echo("2. Generate a token with 'repo' and 'user' scopes.")
        username = click.prompt("Enter your GitHub username")
        token = click.prompt("Enter your GitHub token", hide_input=True)
    
    auth_manager.save_auth("github", {"token": token, "username": username})
    click.secho("✅ GitHub credentials saved!", fg="green")

@auth.command(name="linkedin")
@click.option('--li-at', help='LinkedIn li_at cookie value')
@click.option('--profile-id', help='LinkedIn Profile ID')
@click.pass_obj
def auth_linkedin(auth_manager, li_at, profile_id):
    """Authenticate with LinkedIn."""
    if not li_at or not profile_id:
        click.echo("--- LinkedIn Auth Guide ---")
        click.echo("1. Login to LinkedIn in your browser.")
        click.echo("2. Open DevTools (F12) -> Application -> Cookies.")
        click.echo("3. Copy the 'li_at' cookie value.")
        profile_id = click.prompt("Enter your LinkedIn Profile ID (slug)")
        li_at = click.prompt("Enter your li_at cookie", hide_input=True)
    
    auth_manager.save_auth("linkedin", {"li_at": li_at, "profile_id": profile_id})
    click.secho("✅ LinkedIn credentials saved!", fg="green")

async def _run_extraction(platform_cls: Type[BasePlatform], platform_name: str, auth_manager: AuthManager, output: str):
    config = auth_manager.get_auth(platform_name)
    if not config:
        click.secho(f"❌ No credentials found for {platform_name}. Run 'pulse auth {platform_name}' first.", fg="red")
        return

    platform = platform_cls(config)
    try:
        profile = await platform.extract()
        markdown = platform.to_markdown(profile)
        
        with open(output, "w") as f:
            f.write(markdown)
        
        click.secho(f"✨ Pulse successfully captured {platform_name} identity to {output}", fg="green")
    except Exception as e:
        click.secho(f"💥 Extraction failed: {e}", fg="red", err=True)

@main.command()
@click.option('--output', default='github_pulse.md', help='Output filename')
@click.pass_obj
def github(auth_manager, output):
    """Extract GitHub profile and repository data."""
    asyncio.run(_run_extraction(GitHubPlatform, "github", auth_manager, output))

@main.command()
@click.option('--output', default='linkedin_pulse.md', help='Output filename')
@click.pass_obj
def linkedin(auth_manager, output):
    """Extract LinkedIn activity data."""
    asyncio.run(_run_extraction(LinkedInPlatform, "linkedin", auth_manager, output))

@main.command()
def reddit():
    """Extract Reddit activity (Coming Soon)."""
    click.secho("🚧 Reddit support is coming soon! Stay tuned.", fg="yellow")

if __name__ == "__main__":
    main()
