from typing import Generator

from langchain_community.document_loaders import WebBaseLoader, WikipediaLoader
from langchain_core.documents import Document
from tqdm import tqdm

from philoagents.domain.philosopher import SoccerPlayer, PlayerExtract
from philoagents.domain.philosopher_factory import PlayerFactory


def get_extraction_generator(
    players: list[PlayerExtract],
) -> Generator[tuple[SoccerPlayer, list[Document]], None, None]:
    """Extract documents for a list of players, yielding one at a time.

    Args:
        players: A list of PlayerExtract objects containing player information.

    Yields:
        tuple[SoccerPlayer, list[Document]]: A tuple containing the player object and a list of
            documents extracted for that player.
    """

    progress_bar = tqdm(
        players,
        desc="Extracting docs",
        unit="player",
        bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}",
        ncols=100,
        position=0,
        leave=True,
    )

    player_factory = PlayerFactory()
    for player_extract in progress_bar:
        player = player_factory.get_player(player_extract.id)
        progress_bar.set_postfix_str(f"Player: {player.name}")

        player_docs = extract(player, player_extract.urls)

        yield (player, player_docs)


def extract(player: SoccerPlayer, extract_urls: list[str]) -> list[Document]:
    """Extract documents for a single player from all sources and deduplicate them.

    Args:
        player: SoccerPlayer object containing player information.
        extract_urls: List of URLs to extract content from.

    Returns:
        list[Document]: List of deduplicated documents extracted for the player.
    """

    docs = []

    docs.extend(extract_wikipedia(player))
    docs.extend(extract_web(player, extract_urls))

    return docs


def extract_wikipedia(player: SoccerPlayer) -> list[Document]:
    """Extract documents for a single player from Wikipedia.

    Args:
        player: SoccerPlayer object containing player information.

    Returns:
        list[Document]: List of documents extracted from Wikipedia for the player.
    """

    loader = WikipediaLoader(
        query=player.name,
        lang="en",
        load_max_docs=1,
        doc_content_chars_max=1000000,
    )
    docs = loader.load()

    for doc in docs:
        doc.metadata["player_id"] = player.id
        doc.metadata["player_name"] = player.name

    return docs


def extract_web(
    player: SoccerPlayer, urls: list[str]
) -> list[Document]:
    """Extract documents for a single player from additional web sources.

    Args:
        player: SoccerPlayer object containing player information.
        urls: List of URLs to extract content from.

    Returns:
        list[Document]: List of documents extracted from the web for the player.
    """

    def extract_paragraphs_and_headers(soup) -> str:
        excluded_sections = [
            "bibliography",
            "academic-tools",
            "other-internet-resources",
            "related-entries",
            "acknowledgments",
            "article-copyright",
            "article-banner",
            "footer",
        ]

        for section_name in excluded_sections:
            for section in soup.find_all(id=section_name):
                section.decompose()

            for section in soup.find_all(class_=section_name):
                section.decompose()

            for section in soup.find_all(
                lambda tag: tag.has_attr("id") and section_name in tag["id"].lower()
            ):
                section.decompose()

            for section in soup.find_all(
                lambda tag: tag.has_attr("class")
                and any(section_name in cls.lower() for cls in tag["class"])
            ):
                section.decompose()

        content = []
        for element in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
            content.append(element.get_text())

        return "\n\n".join(content)

    if len(urls) == 0:
        return []

    loader = WebBaseLoader(show_progress=False)
    soups = loader.scrape_all(urls)

    documents = []
    for url, soup in zip(urls, soups):
        text = extract_paragraphs_and_headers(soup)
        metadata = {
            "source": url,
            "player_id": player.id,
            "player_name": player.name,
        }

        if title := soup.find("title"):
            metadata["title"] = title.get_text().strip(" \n")

        documents.append(Document(page_content=text, metadata=metadata))

    return documents


# Keep backward-compatible alias
extract_stanford_encyclopedia_of_philosophy = extract_web


if __name__ == "__main__":
    maradona = PlayerFactory().get_player("maradona")
    docs = extract_wikipedia(maradona)
    print(docs)
