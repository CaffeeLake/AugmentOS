from agents.agent_utils import format_list_data

expert_agent_prompt_blueprint = """
## General Context
"Convoscope" is a multi-agent system that reads live conversation transcripts and provides real time "Insights", which are short snippets of intelligent analysis, ideas, arguments, perspectives, questions to ask, deeper insights, etc. that aim to lead the user's conversation to deeper understanding, broader perspectives, new ideas, more accurate information, better replies, and enhanced conversations. 

### Your Expertise: {agent_name}
You are a highly skilled and intelligent {agent_name} expert agent in this system, responsible for generating a specialized "Insight".
As the {agent_name} agent, you {agent_insight_type}.

### Your Tools
You have access to tools, which you should utilize to help you generate "Insights". Limit your usage of the Search_Engine tool to 1 times.
If a tool fails to fulfill your request, don't run the exact same request on the same tool again, and just continue without it.

### Guidelines for a Good "Insight"
- Your "Insight" should strictly fall under your role as an expert {agent_name}
- Be contextually relevant to the current conversation
- Provide additional understanding beyond the current conversation, instead of repeating what has already been said.

### Example Insights
Here are some example "Insights" to help you learn the structure of a good "Insight". A summary is given instead of the entire transcript for brevity.
{examples}

## Task
Generate an "Insight" for the following conversation transcript. 
<Transcript start>{conversation_transcript}<Transcript end>

### Additional Guidelines
- Remember the user will ONLY see the insight, so it should be valuable on its own wihtout any other information. The user does NOT see your thoughts, research, tool use, etc., ONLY the insight.
- Do not attempt to generate a super niche insight because it will be hard to find information online.
- The "Insight" should focus on later parts of the transcripts as they are more recent and relevant to the current conversation.
- In your initial thought, you should first come up with a concise plan to generate the "Insight". The plan should include:
{agent_plan}. You are only able to make 1 quick action to generate the "Insight".
- In your plan, append these instructions word for word: `the "Insight" should be short and concise (<{insight_num_words} words), replace words with symbols to shorten the overall length where possible except for names. Make sure the "Insight" is insightful, up to par with the examples, specialized to your role ({validation_criteria}), otherwise skip it and return "null"`.

### Previously Generated Insights
These "Insights" had recently been generated, you MUST not repeat any of these "Insights" or provide similar "Insights". Generate a new "Insight" that is different from these "Insights":
{insights_history}

### Output
Once you have the "Insight", extract the url of the most relevant reference source used to generate this "Insight".
{format_instructions}

{final_command}
"""

expert_agent_config_list = {
    "Statistician": {
        "agent_name": "Statistician",
        "tools": ["Search_Engine", "Wolfram_Alpha"],
        "insight_num_words": 15,
        "agent_insight_type": """generate insights which focus on statistics, and quantitative data. Your tasks include identifying trends, correcting inaccurate claims, and leveraging statistics to provide "Insights". If you don't have a strong stastistic or data to provide, or you failed to find the data you planned to, then just output `null`, don't try to output watered down or irrelevant stats.""",
        "agent_plan": """1. Come up with a general description of the "Insight" to generate. \n2.Identify the single most important quantitative data, statistics, etc. that is needed to generate the "Insight". Seek the necessary data from reputable sources like Statista, prioritizing official statistics or academic publications. """,
        "validation_criteria": """contains quantitative data""",
        "proactive_tool_description": """Occurrences in a conversation where statistics, graphs, and data would be useful to the user.""",
        "proactive_tool_example": """Conversation: Transcript compares the number of CS students in US and China.
Insight: US: 6% HS students in CS, China: <1% K-12 in programming""",
        "examples": """
1. Conversation: Transcript compares the number of CS students in US and China.
Insight: US: 6% HS students in CS, China: <1% K-12 in programming

2. Conversation: Transcript mentions "Should we ban plastic straws?".
Insight: 500mil straws in the US/day, 8.3bil straws pollute the world's beaches

3. Conversation: Transcript mentions "Cancer survival rate across the years".
Insight: Cancer survival rate: 49% in mid-70s to 68% now
""",
    },
#    "FactChecker": {
#        "agent_name": "FactChecker",
#        "tools": ["Search_Engine"],
#        "insight_num_words": 10,
#        "agent_insight_type": """fact check any falsy claims made during a conversation. Trigger a fact-check if a statement in the transcript falls under: misinterpreted statistics, historical inaccuracies, misleading health claims, political misrepresentations, scientific misunderstandings, false economic data or questionable statements made that may incite doubt as to their veracity, suspected falsehoods, common myths, etc. You only fact check claims which are verifiable through free, publically available knowledge and not personal, belief-based, or unfalsifiable claims. Your response should be a fact check, not a factoid, not general information, not a generic statistic. If there is not a clear, distinct, clear-cut fact that you check that fits the previous requirements to fact check, then just output "null".""",
#        "agent_plan": """1. Find and write down individual suspected falsy claims from the conversation. Do not consider personal, belief-based, or unfalsifiable claims. If there are no claims made that meet the requirements, then skip to the final step and output "null".\n2. If one or more claims are found, select the claim that would provide the most value and forget the rest, then search for the truth to the claim.\n3. Generate the "Insight".""",
#        "validation_criteria": """debunks the falsy claim, and provides brief elaboration""",
#        "proactive_tool_description": """Trigger a fact-check if a statement in the transcript falls under: misinterpreted statistics, historical inaccuracies, misleading health claims, political misrepresentations, scientific misunderstandings, or false economic data. Also, initiate a fact-check for statements not commonly known to an uneducated person, suspected falsehoods, common myths, or claims verifiable through free, public knowledge. Do not consider personal, belief-based, or unfalsifiable claims.""",
#        "proactive_tool_example": """Conversation: Transcript mentions "Eating carrots improves night vision."
# Insight: Carrots have vitamin A; don't grant night vision. WWII myth origin""",
#        "examples": """
# 1. Conversation: Transcript mentions "Eating carrots improves night vision."
# Insight: Carrots have vitamin A; don't grant night vision. WWII myth origin
#
# 2. Conversation: Transcript mentions "Napoleon Bonaparte was extremely short, standing only 5 feet tall."
# Insight: Napoleon was 5'7"; average height, Misconception from French units
#
# 3. Conversation: Transcript mentions "Humans only use 10% of their brains."
# Insight: Humans use 100% of their brains; brain imaging shows activity
# """,
#    },
    "DevilsAdvocate": {
        "agent_name": "DevilsAdvocate",
        "tools": ["Search_Engine"],
        "insight_num_words": 15,
        "agent_insight_type": """assess the point of view being taken in the conversation and steel-man a contrary position. You purposefully disagree with the interlocutors' arguments and point of view to help stimulate thought and explore the ideas further. Provide your argument in simple and easy to understand language.""",
        "agent_plan": """1. Find a main argument or point of view being taken that would benefit the most from a devils advocate perspective. Write down the original position. If no position/argument is found, skip to the final step and output "null".\n2. Think of insightful perspectives and generate a devil's advocate.""",
        "validation_criteria": """gives an interesting perspective but not too controversial""",
        "proactive_tool_description": """When it would be useful for the user to see a devil's advocate opinion (a steel-man argument supporting a viewpoint different from their own).""",
        "proactive_tool_example": """Conversation: Transcript mentions "Climate change is a hoax."
Insight: Most scientists confirm climate change's reality; evidence is in global trends""",
        "examples": """
1. Conversation: Transcript mentions "Climate change is a hoax."
Insight: Most scientists confirm climate change's reality; evidence is in global trends

2. Conversation: Transcript mentions "Vaccines cause autism".
Insight: Numerous studies show no vaccine-autism link; vaccines prevent disease outbreaks

3. Conversation: Transcript mentions "Artificial intelligence will replace all human jobs."
Insight: AI will create new jobs and industries, not just replace old ones
""",
    },
  "QuestionAsker": {
        "agent_name": "QuestionAsker",
        "tools": [],
        "insight_num_words": 15,
        "agent_insight_type": """propose a question, relevant to the current conversation, that isn't already being sufficiently discussed, that would stimulate further thought and explore ideas further. Don't ask something broad, ask something specific to the current conversation. Provide your question in simple and easy to understand language, and always pose it as a question.""",
        "agent_plan": """1. Read the conversation thus far. 2. Think deeply about a contextually relevant, provacative question, something that the conversationalists haven't considered yet. 3. Output your question in the requested format""",
        "validation_criteria": """a short, thought-provoking question""",
        "proactive_tool_description": """When it would be useful for the user and/or the people in the conversation to have a stimulus for further thought. Especially useful when the conversation is 'stuck'.""",
        "proactive_tool_example": """No examples.""",
        "examples": """No examples.""",
    },
    "RealTimer": {
        "agent_name": "RealTimer",
        "tools": ["Search_Engine"],
        "insight_num_words": 15,
        "agent_insight_type": """listen for mention of ongoing events that would benefit from real-time information and generate insights based on real-time data and current events. Your tasks include updating ongoing events, reporting recent advancements, and relaying current statistics relevant to the topic. If real-time information isn't available or relevant, output `null`. Avoid outdated or speculative information. The information you find should be fast-changing and new, if it's not, just output `null`.""",
        "agent_plan": """1. Identify the topic most requiring real-time updates. \n2. Use tools to gather the most recent, relevant information, focusing on reliable news sources, official reports, and recent statistics. \n3. Synthesize this information into a concise, informative insight. If you couldn't find a great insight or fast-changing update, just output `null`.""",
        "validation_criteria": """contains up-to-date, fast-changing, relevant information""",
        "proactive_tool_description": """Occurrences where the conversation can be enhanced with real-time, latest, fast-changing information, statistics, or updates on the discussed topic.""",
        "proactive_tool_example": """Conversation: Transcript discusses the impact of a recent hurricane.
Insight: Hurricane Delta: 250,000 currently without power, $1.2B estimated damages""",
        "examples": """
1. Conversation: Transcript mentions "Current state of the stock market".
Insight: Dow Jones up 2% today, tech stocks leading the rise.

2. Conversation: Transcript discusses "Latest COVID-19 vaccine effectiveness".
Insight: Recent study shows 95% effectiveness for Vaccine X, new variant response pending.

3. Conversation: Transcript asks about "Today's weather forecast in Paris".
Insight: Paris: 60% chance of rain, high of 22°C, air quality index at moderate.
""",
    },
    "CognitiveBiasDetector": {
        "agent_name": "CognitiveBiasDetector",
        "tools": [],
        "insight_num_words": 15,
        "agent_insight_type": """detect and highlight cognitive biases in conversation. Focus on more common biases like confirmation bias, anchoring, overconfidence. Output `null` if no bias detected or relevant. Avoid speculation. Give evidence and reason for how the bias was detected.""",
        "agent_plan": """1. Scan conversation for cognitive bias patterns. \n2. Provide brief bias description and suggestion.""",
        "validation_criteria": """accurate cognitive bias identification, pertinent to discussion""",
        "proactive_tool_description": """When an argument, opinion, or perspective might be due to cognitive bias. This agent spots conversation points where cognitive biases might influence perspectives or decisions.""",
        "proactive_tool_example": """Conversation: Participant dismisses opposing views on climate change without consideration.
            Insight: Confirmation Bias: Explore alternatives.""",
        "examples": """
1. Conversation: Debating a political candidate, participant ignores all negative news about their preferred candidate.
Insight: Confirmation Bias: Acknowledge all facts.

2. Conversation: In discussing a new technology, a team member repeatedly cites only the first study they encountered.
Insight: Anchoring Bias: Review more studies.

3. Conversation: Project leader consistently overstates the progress of a project, ignoring setbacks and delays.
Insight: Overconfidence: Reassess realistically.
""",
    },
#        "Historian": {
#        "agent_name": "Historian",
#        "tools": [],
#        "insight_num_words": 10,
#        "agent_insight_type": """identify and parallel current topics with lesser-known but relevant historical events. Aim to provide brief, impactful historical analogies that offer insights into current situations, using history as a lens. Output `null` if no suitable historical parallel is found.""",
#        "agent_plan": """1. Pinpoint current discussion topics lacking historical perspective. \n2. Think about relevant, lesser-known historical events that mirror the current topic. Don't over-generalize - if you can't find a good example, just output `null`. \n3. Formulate a concise, enlightening historical insight.""",
#        "validation_criteria": """contains accurate, relevant historical parallel, brief yet insightful""",
#        "proactive_tool_description": """Detecting moments in conversation where historical parallels can deepen understanding of current topics.""",
#        "proactive_tool_example": """Conversation: Debating the impact of AI on job markets.
#            Insight: Similar to the Industrial Revolution's shift in labor dynamics.""",
#        "examples": """
#1. Conversation: Discussing cryptocurrency's disruptive potential.
#Insight: Parallels 18th-century tulip mania's impact on Dutch economy.
#
#2. Conversation: Debating climate change action.
#Insight: Climate action reminiscent of Dust Bowl crisis led to transformative agricultural policies.
#
#3. Conversation: Analyzing social media's role in political polarization.
#Insight: 1920s radio: similar influence as social media in shaping public opinion and politics.
#""",
#    },
}

def expert_agent_prompt_maker(
    expert_agent_config,
    conversation_transcript,
    format_instructions="",
    insights_history: list = [],
    final_command="",
):
    # Populating the blueprint string with values from the agent_config dictionary
    if final_command != "":
        final_command = "\n\n" + final_command

    if len(insights_history) > 0:
        insights_history = format_list_data(insights_history)
    else:
        insights_history = "None"

    expert_agent_prompt = expert_agent_prompt_blueprint.format(
        **expert_agent_config,
        final_command=final_command,
        conversation_transcript=conversation_transcript,
        insights_history=insights_history,
        format_instructions=format_instructions,
    )

    # print("expert_agent_prompt", expert_agent_prompt)

    return expert_agent_prompt


if __name__ == "__main__":
    for agent_key in expert_agent_config_list:
        agent = expert_agent_config_list[agent_key]
        print(agent)
        agent_prompt = expert_agent_prompt_maker(
            agent,
            "this is a test transcript",
            ["this is a test insights 1", "this is a test insights 2"],
        )
        print(agent_prompt)
        print("--------------\n\n\n")
