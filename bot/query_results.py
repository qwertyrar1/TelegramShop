from aiogram.types import InlineQueryResultArticle, InputTextMessageContent, LinkPreviewOptions
from secrets import token_hex


def get_query_results():
    return [
        InlineQueryResultArticle(
            id=token_hex(2),
            title='Вопрос 1',
            description='Текст Вопроса 1',
            input_message_content=InputTextMessageContent(
                message_text='Текст Вопроса 1',
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                disable_web_page_preview=True
            )
        ),
        InlineQueryResultArticle(
            id=token_hex(2),
            title='Вопрос 2',
            description='Текст Вопроса 2',
            input_message_content=InputTextMessageContent(
                message_text='Текст Вопроса 2',
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                disable_web_page_preview=True
            )
        ),
        InlineQueryResultArticle(
            id=token_hex(2),
            title='Вопрос 3',
            description='Текст Вопроса 3',
            input_message_content=InputTextMessageContent(
                message_text='Текст Вопроса 3',
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                disable_web_page_preview=True
            )
        )
    ]