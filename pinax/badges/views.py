from collections import defaultdict

from django.db.models import Count
from django.shortcuts import render

from .models import BadgeAward
from .registry import badges


def badge_list(request):
    if request.user.is_authenticated:
        user_badges = set(
            (slug, level) for slug, level in
            BadgeAward.objects.filter(user=request.user).values_list("slug", "level")
        )
    else:
        user_badges = []
    badges_awarded = BadgeAward.objects.values("slug", "level").annotate(num=Count("pk"))
    badges_dict = defaultdict(list)
    for badge in badges_awarded:
        name = None
        description = None
        image = None
        points = None
        points_next = None
        required_badges = None

        if badge['slug'] in badges._registry:
            if badge['level'] in badges._registry[badge["slug"]].levels:
                name = badges._registry[badge["slug"]].levels[badge["level"]].name
        if badge['slug'] in badges._registry:
            if badge['level'] in badges._registry[badge["slug"]].levels:
                description = badges._registry[badge["slug"]].levels[badge["level"]].description
        if badge['slug'] in badges._registry:
            if badge['level'] in badges._registry[badge["slug"]].levels:
                image = badges._registry[badge["slug"]].levels[badge["level"]].image
        if badge['slug'] in badges._registry:
            if badge['level'] in badges._registry[badge["slug"]].levels:
                points = badges._registry[badge["slug"]].levels[badge["level"]].points
        if badge['slug'] in badges._registry:
            if badge['level'] in badges._registry[badge["slug"]].levels:
                points_next = badges._registry[badge["slug"]].levels[badge["level"]].points_next
        if badge['slug'] in badges._registry:
            if badge['level'] in badges._registry[badge["slug"]].levels:
                required_badges = badges._registry[badge["slug"]].levels[badge["level"]].required_badges

        badges_dict[badge["slug"]].append({
            "level": badge["level"],
            "name": name,
            "description": description,
            "image": image,
            "points": points,
            "points_next": points_next,
            "required_badges": required_badges,
            "count": badge["num"],
            "user_has": (badge["slug"], badge["level"]) in user_badges
        })

    for badge_group in badges_dict.values():
        badge_group.sort(key=lambda o: o["level"])

    return render(request, "phileo/badges/badges.html", {
        "badges": sorted(badges_dict.items()),
    })


def badge_detail(request, slug, level):
    if slug in badges._registry:
        if int(level) in badges._registry[slug].levels:
            badge = badges._registry[slug].levels[int(level)]
    # badge = badges._registry[slug].levels[int(level)]
    badge_awards = BadgeAward.objects.filter(
        slug=slug,
        level=level
    ).order_by("-awarded_at")

    badge_count = badge_awards.count()
    latest_awards = badge_awards[:50]

    return render(request, "phileo/badges/badge_detail.html", {
        "badge": badge,
        "badge_count": badge_count,
        "latest_awards": latest_awards,
    })
