$(function () {
    // 获取所有侧边栏列表项元素
    const sidebarframeItems = $('.sidebar-frame a.list-group-item');
    // 获取侧边栏搜索框元素
    const searchBox = $('.sidebar-frame input[type="search"]');
    // 给搜索框元素添加 input 事件监听器
    searchBox.on('input', () => {
        // 获取搜索框中的关键字并去除两侧空格
        const keyword = searchBox.val().trim();
        // 判断搜索框是否为空
        if (!keyword) {
            // 如果搜索框为空则将所有列表项元素都显示出来
            sidebarframeItems.show();
        } else {
            // 否则隐藏所有列表项元素，并根据关键字过滤符合条件的元素并显示出来
            sidebarframeItems.hide().filter((_, item) => {
                // 获取列表项文本，并将该文本中的中英文全角和半角字符替换为小写，以方便后续匹配
                let allLowerCaseText = $(item).text().trim().toLowerCase();
                allLowerCaseText = allLowerCaseText.replace(/[^\x00-\xff]/g, (char) => {
                    let charCode = char.charCodeAt(0);
                    if (charCode === 12288) {
                        return String.fromCharCode(32);
                    } else if (charCode > 65280 && charCode < 65375) {
                        return String.fromCharCode(charCode - 65248);
                    }
                    return char;
                });
                // 获取关键字，并将中英文全角和半角字符替换为小写，以方便后续匹配
                let allLowerCaseKeyword = keyword.toLocaleLowerCase();
                allLowerCaseKeyword = allLowerCaseKeyword.replace(/[^\x00-\xff]/g, (char) => {
                    let charCode = char.charCodeAt(0);
                    if (charCode === 12288) {
                        return String.fromCharCode(32);
                    } else if (charCode > 65280 && charCode < 65375) {
                        return String.fromCharCode(charCode - 65248);
                    }
                    return char;
                });
                // 匹配列表项文本和关键字，如果找到符合条件的则返回 true，否则返回 false
                if (allLowerCaseText.includes(allLowerCaseKeyword)) {
                    return true;
                } else {
                    return false;
                }
            }).show();
        }
    });
});
