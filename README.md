# translate-cli

## Pre-requirements

- [python3](https://www.python.org/)
- python3-pip

## Install

```shell
bash install.sh
```

## Usage

```shell
$ trans --help
Usage:
    trans [<EN_WORD|ZH-CN_WORD> ...]

```

## Example

```shell
$ trans hello 世界
┌──
│   hello
│   英 [həˈləʊ] 美 [heˈloʊ]
│   int. 喂，你好（用于问候或打招呼）；喂，你好（打电话时的招呼语）；喂，你好（引起别人注意的招呼语）；<非正式>喂，嘿 (认为别人说了蠢话或分心)；<英，旧>嘿（表示惊讶）
│   n. 招呼，问候；（Hello）（法、印、美、俄）埃洛（人名）
│   v. 说（或大声说）“喂”；打招呼
│   [复数 hellos 第三人称单数 helloes 现在分词 helloing 过去式 helloed 过去分词 helloed]
│   https://dict.youdao.com/result?word=hello&lang=en
└──
┌──
│   world
│   英 [wɜːld] 美 [wɜːrld]
│   n. 地球，天下（the world）；（尤指可能或确有生命存在的）星球，天体；（某地区、某类人及事物组成的）世界；人类社会，社会生活；（人们活动的）领域，界，圈子； 某领域的一切事物，自然界；人的）地方，（某种生活的）世界；<非正式>大量，无数；一切，重要性（the world）
│   adj. （人物）举足轻重的，世界闻名的；所有国家的，世界（性）的；环球的
│   
│   https://dict.youdao.com/result?word=world&lang=en
├──
│   earth
│   英 [ɜːθ] 美 [ɜːrθ]
│   n. 地球，世界；陆地，地面；泥土，土壤；地线，电线；<英，非正式>一大笔钱；尘世；兽穴
│   v. 把（电线）接地；用土掩盖；追赶入洞穴
│   [复数 earths 第三人称单数 earths 现在分词 earthing 过去式 earthed 过去分词 earthed]
│   https://dict.youdao.com/result?word=earth&lang=en
├──
│   welt
│   英 [welt] 美 [welt]
│   n. 贴边，[服装]沿条；鞭痕；殴打
│   vt. 加沿条于……；使……留下鞭痕；对……进行殴打
│   n. （Welt）人名；（英、德、罗）韦尔特
│   [复数 welts 第三人称单数 welts 现在分词 welting 过去式 welted 过去分词 welted]
│   https://dict.youdao.com/result?word=welt&lang=en
└──
```

```shell
$ trans
Youdao Dictionary CLI Interactor
────────────────────────────────
Type the words (zh-cn, en) you want to query.
Type "exit()", "quit()" or CTRL-C to exit the interactor.
>>> 你好 world
┌──
│   hello
│   英 [həˈləʊ] 美 [heˈloʊ]
│   int. 喂，你好（用于问候或打招呼）；喂，你好（打电话时的招呼语）；喂，你好（引起别人注意的招呼语）；<非正式>喂，嘿 (认为别人说了蠢话或分心)；<英，旧>嘿（表示惊讶）
│   n. 招呼，问候；（Hello）（法、印、美、俄）埃洛（人名）
│   v. 说（或大声说）“喂”；打招呼
│   [复数 hellos 第三人称单数 helloes 现在分词 helloing 过去式 helloed 过去分词 helloed]
│   https://dict.youdao.com/result?word=hello&lang=en
├──
│   hi
│   英 [haɪ] 美 [haɪ]
│   int. 嗨！（表示问候或用以唤起注意）
│   n. （Hi）人名；（柬）希
│   
│   https://dict.youdao.com/result?word=hi&lang=en
├──
│   how do you do
│    
│   你好
│   
│   https://dict.youdao.com/result?word=how%20do%20you%20do&lang=en
└──
┌──
│   world
│   英 [wɜːld] 美 [wɜːrld]
│   n. 地球，天下（the world）；（尤指可能或确有生命存在的）星球，天体；（某地区、某类人及事物组成的）世界；人类社会，社会生活；（人们活动的）领域，界，圈子； 某领域的一切事物，自然界；人生，生活圈子，阅历； 人世，今生，来世；生活领域；尘世，世俗，世事（the world）；社会地位；活的状态；大不相同；（尤指某人描述或想象的）地方，情景；（有某种特色的）地方，（某种生活的）世界；<非正式>大量，无数；一切，重要性（the world）
│   adj. （人物）举足轻重的，世界闻名的；所有国家的，世界（性）的；环球的
│   
│   https://dict.youdao.com/result?word=world&lang=en
└──
>>> 
```