
from models.poll import Poll
import matplotlib.pyplot as plt

def pie_chart(polls_id: list):
    try:
        figure = plt.figure()
        rows = (len(polls_id) // 3) + 1
        if len(polls_id) > 3:
            columns = 3
        else:
            columns = len(polls_id)
        for i_poll, poll_id in enumerate(polls_id, start = 1):
            poll = Poll.get(poll_id)
            options = poll.options

            option_name = [option.text for option in options]
            option_number = [len(option.votes) for option in options]

            axes = figure.add_subplot(rows, columns, i_poll)
            axes.pie(
                option_number,
                labels = option_name,
                autopct = "%1.1f%%")

            axes.set_title(poll.title)
    finally:
        plt.show()

def column_chart(polls_id: list):
    figure = plt.figure()
    poll_titles = []
    poll_votes = []
    for poll_id in polls_id:
        poll = Poll.get(poll_id)
        poll_titles.append(poll.title)
        poll_votes.append(poll.all_votes())

    print(poll_titles)
    print(poll_votes)
    axes = figure.add_subplot()
    axes.bar(
        [x for x in range(len(polls_id))],
        poll_votes,
        tick_label = poll_titles
    )
    plt.show()


if __name__ == '__main__':
    pie_chart([1, 4, 3, 5])
    column_chart([1,3,4])