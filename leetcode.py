# conding=utf-8
# ※Author = 胡志达
# ※Time = 2022/3/4 17:48
# ※File Name = leetcode.py
# ※Email = 840831038@qq.com


nums = [1,2]
k = 5

nums = nums[len(nums)-k:len(nums)] + nums[0:len(nums)-k]


print(nums)