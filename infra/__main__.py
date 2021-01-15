import pulumi
import pulumi_aws as aws


cat_weather_intent = aws.lex.Intent(
    'CatWeatherIntent',
    description='Intent to determine if the weather is suitable for cat to go out',
    name='CatWeatherIntent',
    create_version=False,
    confirmation_prompt=aws.lex.IntentConfirmationPromptArgs(
        max_attempts=2,
        messages=[{
            'content': 'So you want to know if your cat can go out today in {City}?',
            'content_type': 'PlainText'
        }]
    ),
    rejection_statement=aws.lex.IntentRejectionStatementArgs(
        messages=[{
            'content': 'Sorry, can you please repeat your initial question?',
            'content_type': 'PlainText'
        }]
    ),
    fulfillment_activity=aws.lex.IntentFulfillmentActivityArgs(
        type='ReturnIntent'
    ),
    sample_utterances=[
        'Can my cat go outside',
        'Is it warm enough for my cat',
        'Can I let my cat out in {City}',
        'Should my cat wear booties in {City}',
        'Will my cat stay dry in {City}'
    ],
    slots=[
        aws.lex.IntentSlotArgs(
            description='The city where the cat lives',
            name='City',
            priority=1,
            slot_constraint='Required',
            slot_type='AMAZON.US_CITY',
            value_elicitation_prompt=aws.lex.IntentSlotValueElicitationPromptArgs(
                max_attempts=2,
                messages=[{
                    'content': 'Which city?',
                    'content_type': 'PlainText'
                }]
            )
        )
    ]
)

cat_weather_bot = aws.lex.Bot(
    'CatWeatherBot',
    description='Bot to determine if the cat can go out',
    name='CatWeatherBot',
    create_version=False,
    process_behavior='BUILD',
    enable_model_improvements=True,
    child_directed=False,
    idle_session_ttl_in_seconds=600,
    clarification_prompt=aws.lex.BotClarificationPromptArgs(
        max_attempts=2,
        messages=[{
            'content': 'I did not understand you, what would you like to do?',
            'content_type': 'PlainText'
        }]
    ),
    abort_statement=aws.lex.BotAbortStatementArgs(
        messages=[{
            'content': 'Sorry, I am not able to assist at this time',
            'content_type': 'PlainText'
        }]
    ),
    intents=[
        aws.lex.BotIntentArgs(
            intent_name=cat_weather_intent.name,
            intent_version=cat_weather_intent.version
        )
    ],
    locale='en-US',
    voice_id='Salli'
)
