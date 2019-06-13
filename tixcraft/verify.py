from itertools import combinations
from multiprocessing import Pool
from lxml import etree
import os
import re
from tixcraft.driver import user_verify
from tixcraft import parser


class IncorrectCheckCodeError(RuntimeError):
    pass


class Verifier:
    def __init__(self, session, source_code):
        self.session = session
        self.CSRFTOKEN = parser.CSRFTOKEN(source_code)
        self.checkcode_url = parser.checkcode_url(source_code)
        self.source_code = source_code

    def _replace_noise(self, question):
        question = re.sub(r"<[^>]*>", "", question)
        for noise in ["&#13", "\n", ";", " "]:
            question = question.replace(noise, "")
        return question

    def _reduce_noise(self, questions):
        questions = [question for question in questions if len(question) >= 3]
        return questions

    def _extract_questions(self, form):
        question = re.sub(r"<br/*>", "|", form)
        question = self._replace_noise(question)
        questions = question.split("||")
        questions = [question.split("|") for question in questions]
        questions = self._reduce_noise(questions)
        return questions

    def _is_option(self, option):
        MATCHES = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvwxyz"
            "0123456789"
            "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
            "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
            "０１２３４５６７８９"
        )
        if len(option) < 3:
            return False
        option = option[:4]
        for each in option:
            if each in MATCHES:
                return True
        return False

    def _extract_options(self, questions):
        options = []
        for question in questions:
            options.append([line for line in question if self._is_option(line)])
        return options

    def _extract_codes(self, options):
        MATCHES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "abcdefghijklmnopqrstuvwxyz" "0123456789"
        FULLWIDTH_MATCHES = (
            "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ" "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ" "０１２３４５６７８９"
        )
        MATCHES += FULLWIDTH_MATCHES

        codes = []
        for option in options:
            code = []
            for each in option:
                for char in each:
                    if char in MATCHES:
                        if char in FULLWIDTH_MATCHES:
                            char = MATCHES[FULLWIDTH_MATCHES.index(char)]
                        code.append(char)
                        break
            codes.append(code)
        return codes

    def _combine(self, combined_codes):
        combined_codes = combined_codes.copy()
        codes = combined_codes.pop(0)
        codes = codes.copy() + [("",)]
        if not combined_codes:
            return codes
        new_codes = []
        for code in codes:
            new_codes += [code + new_code for new_code in self._combine(combined_codes)]
        return new_codes

    def _checkCodes(self, codes):
        return ["".join(code) for code in codes]

    def _muti_choice(self, codes):
        combined_codes = [list(combinations(code, 1)) for code in codes]
        return combined_codes

    def _muti_selection(self, codes):
        combined_codes = []
        for code in codes:
            combined_code = []
            for i in range(1, len(code) + 1):
                combined_code += list(combinations(code, i))
            combined_codes.append(combined_code)
        return combined_codes

    def _brute_force(self, checkCodes):
        print(f"開始進行verify暴力破解，共有{len(checkCodes)}個答案組合")
        processes = os.cpu_count() * 2
        pool = Pool(processes=processes)
        results = pool.map_async(self._verify, checkCodes)
        results.wait()
        results = results.get()
        pool.close()
        pool.join()
        return results

    def _verify(self, checkCode):
        data = {
            "CSRFTOKEN": self.CSRFTOKEN,
            "checkCode": checkCode,
            "confirmed": "true",
        }
        try:
            r = self.session.post(self.checkcode_url, data=data)
            url = parser.json_url(r.text)
            if url is None:
                raise IncorrectCheckCodeError()
            result = {"url": url, "checkCode": checkCode}
        except:
            result = None
        return result

    def _undefined(self, driver, url):
        url = user_verify(driver, url)
        return url

    def _choice(self):
        html = etree.HTML(self.source_code)
        form = html.xpath("//form")[0]
        form = etree.tostring(form, encoding="unicode")
        questions = self._extract_questions(form)
        options = self._extract_options(questions)
        codes = self._extract_codes(options)
        if "複選" in form:
            combined_codes = self._muti_selection(codes)
        else:
            combined_codes = self._muti_choice(codes)

        combined_codes = self._combine(combined_codes)
        checkCodes = self._checkCodes(combined_codes)
        if len(checkCodes) <= 1:
            result = None
            return result

        results = self._brute_force(checkCodes)
        results = list(filter(lambda result: result is not None, results))
        if len(results):
            result = results[0]
        else:
            result = None
        return result

    def _copy_paste(self):
        html = etree.HTML(self.source_code)
        result = None
        try:
            checkcode = html.xpath("//font/text()")[-1]
            result = self._verify(checkcode)
        except IndexError:
            pass
        return result

    def _result(self, result):
        url = result["url"]
        print("checkCode:", result["checkCode"])
        return url

    def run(self, driver, verify_url):
        result = self._copy_paste()
        if result:
            url = self._result(result)
            return "https://tixcraft.com" + url

        result = self._choice()
        if result:
            url = self._result(result)
            return "https://tixcraft.com" + url

        url = self._undefined(driver, verify_url)
        return url
