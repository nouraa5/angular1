from django.contrib.auth.models import User, Group

from rest_framework import serializers


class SignupFormSerializer(serializers.Serializer):
    group = serializers.ChoiceField(choices=[(
        group.id, group.name) for group in Group.objects.filter(name__in=['Seller', 'Buyer'])])

    username = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception=raise_exception)
        if is_valid:
            if self.initial_data.get('password1') != self.initial_data.get('password2'):
                self._errors['password'] = ['Passwords do not match']
                if raise_exception:
                    raise serializers.ValidationError(self.errors)
                return False

            email = self.initial_data.get('email')
            if User.objects.filter(email=email).exists():
                self._errors['email'] = ['email is already used']
                if raise_exception:
                    raise serializers.ValidationError(self.errors)
                return False

        return is_valid

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password1']
        group_id = validated_data['group']

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        group = Group.objects.get(id=group_id)
        user.groups.add(group)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
