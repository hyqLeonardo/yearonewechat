from yearonequant.event import *
from yearonequant.event_object import *

from subprocess import call
import os.path
import re


def previous_days_event2file(days_before_today):
    """
    Keep only days before today's event, save to a separate file
    :param days_before_today:   number of days before today
    :return:    file path of written file
    """

    print("generating previous {} days event csv file..."
          .format(days_before_today))

    today = datetime.datetime.now() - datetime.timedelta(days=1)
    start_date = today - datetime.timedelta(days=days_before_today)

    today_str = datetime2ymd_str(today)
    start_str = datetime2ymd_str(start_date)
    write_file_path = './file/events_from_{}_to_{}.csv'\
        .format(start_str-datetime.timedelta(days=1), today_str)

    # return if already has the file
    if os.path.isfile(write_file_path):
        return write_file_path

    fd = open(write_file_path, "wb")
    pattern_argument = "0,/{}/p".format(start_str)
    call(["sed", "-n", pattern_argument,
          "../Documents/announcements_abstract.csv"], stdout=fd)

    print('file saved as {}'.format(write_file_path))
    return write_file_path


def event_to_push2file(event_name, days_before_today=7):
    """
    Save specific events into human-readable format, for pushing to wechat user.
    :param event_name:          event name
    :param days_before_today:   number of days to look back
    :return:    void
    """

    if event_name not in ALL_EVENTS:
        print("event {} has not been defined yet".format(event_name))
        return

    event_dict = ALL_EVENTS.get(event_name)
    print("generating {} event list...".format(event_name))

    announce_path = str(previous_days_event2file(days_before_today))

    matcher_start = re.match('.+from_(.+)_to.+', announce_path)
    matcher_end = re.match('.+to_(.+)\.csv', announce_path)
    start_str = matcher_start.group(1)
    today_str = matcher_end.group(1)

    write_file_path = './file/{}_{}.txt'.format(event_name, today_str)
    write_fd = open(write_file_path, 'w+')
    write_fd.write("以下是从{}到{}的所有{}事件\n"
                   "点击蓝色的\"公告标题\"可以下载公告文件\n\n"
                   .format(start_str, today_str, event_dict.chinese_name))

    df = read_announce_csv(announce_path)

    target_words = event_dict.target_words
    filter_words = event_dict.filter_words
    filter_mode = event_dict.filter_mode

    count = 0
    # loop over rows of df
    for date, row in df.iterrows():
        code = complete_code(str(row['Code']))
        # code has meaning and title pass the filter
        if date and code and filter_title(row['Title'], target_words, filter_words, filter_mode):
            title_url = "<a href=\"{}\">{}</a>".format(row['Link'], row['Title'])
            line = "股票代码:{}, 公告标题:{}, 发布时间:{}\n\n".format(code, title_url, date)
            write_fd.write(line)
            count += 1

    print("{} {} events, file saved as {}".format(count, event_name, write_file_path))

if __name__ == '__main__':

    for event_name in ALL_EVENTS:
        print("now generating event list file for {}...".format(event_name))
        event_to_push2file(event_name)
