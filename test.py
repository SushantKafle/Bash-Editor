import re
data = r'''
        menu_item = 'casserole';
        menu_item = 'meat 
                    loaf';
        menu_item = 'Tony\'s magic pizza';
        menu_item = 'hamburger';
        menu_item = 'Dave\'s famous pizza';
        menu_item = 'Dave\'s lesser-known
            gyro';'''

re_sq_short = r"'([^'\\]*(?:\\.[^'\\]*)*)'"

matches = re.finditer(re_sq_short, data, re.DOTALL | re.VERBOSE)

for m in matches:
    print m.start(0)
#print matches
