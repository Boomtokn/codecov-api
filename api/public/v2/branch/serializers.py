from rest_framework import serializers

from api.public.v2.commit.serializers import CommitDetailSerializer
from core.models import Branch, Commit


class BranchSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    updatestamp = serializers.DateTimeField()

    class Meta:
        model = Branch
        fields = ("name", "updatestamp")


class BranchDetailSerializer(BranchSerializer):
    head_commit = serializers.SerializerMethodField()

    def get_head_commit(self, branch: Branch):
        commit = (
            Commit.objects.filter(
                repository_id=branch.repository_id, commitid=branch.head
            )
            .defer("report")
            .first()
        )
        return CommitDetailSerializer(commit).data

    class Meta:
        model = Branch
        fields = BranchSerializer.Meta.fields + ("head_commit",)
