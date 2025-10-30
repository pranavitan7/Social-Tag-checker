import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box

# Initialize Console
console = Console()

# Function to fetch social tags from the website
def fetch_social_tags(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url  # Default to HTTP if protocol is missing

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        soup = BeautifulSoup(response.text, "html.parser")

        metadata = {
            # Basic Meta Tags
            "Title": soup.title.string if soup.title else "N/A",
            "Description": soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "N/A",
            "Keywords": soup.find("meta", attrs={"name": "keywords"})["content"] if soup.find("meta", attrs={"name": "keywords"}) else "N/A",
            "Canonical URL": soup.find("link", attrs={"rel": "canonical"})["href"] if soup.find("link", attrs={"rel": "canonical"}) else "N/A",

            # OpenGraph Tags
            "OG Title": soup.find("meta", attrs={"property": "og:title"})["content"] if soup.find("meta", attrs={"property": "og:title"}) else "N/A",
            "OG Type": soup.find("meta", attrs={"property": "og:type"})["content"] if soup.find("meta", attrs={"property": "og:type"}) else "N/A",
            "OG Image": soup.find("meta", attrs={"property": "og:image"})["content"] if soup.find("meta", attrs={"property": "og:image"}) else "N/A",
            "OG URL": soup.find("meta", attrs={"property": "og:url"})["content"] if soup.find("meta", attrs={"property": "og:url"}) else "N/A",
            "OG Description": soup.find("meta", attrs={"property": "og:description"})["content"] if soup.find("meta", attrs={"property": "og:description"}) else "N/A",

            # Twitter Tags
            "Twitter Card": soup.find("meta", attrs={"name": "twitter:card"})["content"] if soup.find("meta", attrs={"name": "twitter:card"}) else "N/A",
            "Twitter Site": soup.find("meta", attrs={"name": "twitter:site"})["content"] if soup.find("meta", attrs={"name": "twitter:site"}) else "N/A",
            "Twitter Creator": soup.find("meta", attrs={"name": "twitter:creator"})["content"] if soup.find("meta", attrs={"name": "twitter:creator"}) else "N/A",
            "Twitter Title": soup.find("meta", attrs={"name": "twitter:title"})["content"] if soup.find("meta", attrs={"name": "twitter:title"}) else "N/A",
            "Twitter Image": soup.find("meta", attrs={"name": "twitter:image"})["content"] if soup.find("meta", attrs={"name": "twitter:image"}) else "N/A",

            # Miscellaneous
            "Theme Color": soup.find("meta", attrs={"name": "theme-color"})["content"] if soup.find("meta", attrs={"name": "theme-color"}) else "N/A",
            "Viewport": soup.find("meta", attrs={"name": "viewport"})["content"] if soup.find("meta", attrs={"name": "viewport"}) else "N/A",
            "Author": soup.find("meta", attrs={"name": "author"})["content"] if soup.find("meta", attrs={"name": "author"}) else "N/A",
            "Favicon": soup.find("link", attrs={"rel": "icon"})["href"] if soup.find("link", attrs={"rel": "icon"}) else "N/A",
        }

        return metadata

    except requests.exceptions.RequestException as e:
        return {"Error": f"Failed to fetch data: {str(e)}"}

# Function to display the fetched results in a table format
def display_results(metadata):
    table = Table(title="🔎 Social Tags Information", style="bold cyan", box=box.ROUNDED)

    table.add_column("Tag", style="bold yellow")
    table.add_column("Value", style="bold white", overflow="fold")

    if "Error" in metadata:
        table.add_row("Error", f"[red]{metadata['Error']}[/red]")
    else:
        for key, value in metadata.items():
            table.add_row(key, f"[green]{value}[/green]" if value != "N/A" else "[red]N/A[/red]")

    console.print(table)

# Function to display welcome message in table format
def display_welcome():
    table = Table(title="🚀 Welcome to the Social Tag Tool 🚀", style="bold cyan", box=box.ROUNDED)

    table.add_column("Author", style="bold yellow")
    table.add_column("Details", style="bold white")

    table.add_row("Author", "G16")
    table.add_row("Tool", "Social Tags Scraper")

    console.print(table)

# Main function
def main():
    # Display welcome message in a table format
    display_welcome()

    # Ask the user for a URL
    url = Prompt.ask("Enter website URL (with or without https://)", default="https://example.com")

    metadata = fetch_social_tags(url)
    display_results(metadata)

# Run the main function
if __name__ == "__main__":
    main()
