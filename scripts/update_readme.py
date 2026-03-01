import urllib.request
import xml.etree.ElementTree as ET
import re
from datetime import datetime

# URL of the minimalist innovation RSS feed
FEED_URL = "https://www.minimalistinnovation.com/blog/blog-feed.xml"


def fetch_blog_posts():
    try:
        # Fetch the XML feed using built-in urllib
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()

        # Parse the XML using built-in ElementTree
        root = ET.fromstring(xml_data)
        posts = []

        # Standard RSS feed structure has <item> elements inside <channel>
        for item in root.findall(".//item"):
            title_elem = item.find("title")
            link_elem = item.find("link")

            if title_elem is not None and link_elem is not None:
                title = title_elem.text
                url = link_elem.text
                posts.append({"title": title, "url": url})

        # Limit to the latest 10 posts
        return posts[:10]
    except Exception as e:
        print(f"Error fetching blog posts: {e}")
        return []


def update_readme(posts):
    with open("profile/README.template.md", "r", encoding="utf-8") as file:
        template = file.read()

    # Generate the markdown string for the posts
    posts_md = ""
    if posts:
        for post in posts:
            posts_md += f"- [{post['title']}]({post['url']})\n"
    else:
        posts_md = "- *No recent blog posts found.*\n"

    # Replace the placeholder with the new content using regex
    # The template should have <!-- BLOG-POSTS:START --> ... <!-- BLOG-POSTS:END -->
    template = re.sub(
        r"<!-- BLOG-POSTS:START -->.*<!-- BLOG-POSTS:END -->",
        f"<!-- BLOG-POSTS:START -->\n{posts_md}<!-- BLOG-POSTS:END -->",
        template,
        flags=re.DOTALL,
    )

    # Update the date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    template = re.sub(
        r"<!-- DATE:START -->.*<!-- DATE:END -->",
        f"<!-- DATE:START -->{current_date}<!-- DATE:END -->",
        template,
        flags=re.DOTALL,
    )

    with open("profile/README.md", "w", encoding="utf-8") as file:
        file.write(template)
    print("profile/README.md has been successfully updated.")


if __name__ == "__main__":
    latest_posts = fetch_blog_posts()
    print(f"Found {len(latest_posts)} posts.")
    update_readme(latest_posts)
