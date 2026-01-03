from django.core.management.base import BaseCommand
from django.utils.text import slugify
from quotes.models import Category, Quote


class Command(BaseCommand):
    help = 'Populate the database with motivational quotes and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Success', 'description': 'Quotes about achieving success and reaching goals'},
            {'name': 'Resilience', 'description': 'Quotes about overcoming challenges and bouncing back'},
            {'name': 'Growth', 'description': 'Quotes about personal development and learning'},
            {'name': 'Courage', 'description': 'Quotes about bravery and taking risks'},
            {'name': 'Mindfulness', 'description': 'Quotes about being present and self-aware'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={'name': cat_data['name'], 'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_data["name"]}'))

        self.stdout.write('Creating quotes...')
        quotes_data = [
            # Success quotes
            ('The only way to do great work is to love what you do.', 'Steve Jobs', 'Success'),
            ('Success is not final, failure is not fatal: it is the courage to continue that counts.', 'Winston Churchill', 'Success'),
            ('The secret of success is to do the common thing uncommonly well.', 'John D. Rockefeller Jr.', 'Success'),
            ('Success usually comes to those who are too busy to be looking for it.', 'Henry David Thoreau', 'Success'),
            ('Don\'t be afraid to give up the good to go for the great.', 'John D. Rockefeller', 'Success'),
            ('I find that the harder I work, the more luck I seem to have.', 'Thomas Jefferson', 'Success'),
            ('Success is walking from failure to failure with no loss of enthusiasm.', 'Winston Churchill', 'Success'),
            ('The way to get started is to quit talking and begin doing.', 'Walt Disney', 'Success'),
            ('The road to success and the road to failure are almost exactly the same.', 'Colin R. Davis', 'Success'),
            ('Success is not how high you have climbed, but how you make a positive difference to the world.', 'Roy T. Bennett', 'Success'),
            ('Don\'t watch the clock; do what it does. Keep going.', 'Sam Levenson', 'Success'),
            ('The only place where success comes before work is in the dictionary.', 'Vidal Sassoon', 'Success'),
            ('Success is getting what you want, happiness is wanting what you get.', 'W. P. Kinsella', 'Success'),
            ('Success is not the key to happiness. Happiness is the key to success.', 'Albert Schweitzer', 'Success'),
            ('I never dreamed about success, I worked for it.', 'Estee Lauder', 'Success'),
            ('Success seems to be connected with action. Successful people keep moving.', 'Conrad Hilton', 'Success'),
            ('The difference between who you are and who you want to be is what you do.', 'Bill Phillips', 'Success'),
            ('Opportunities don\'t happen. You create them.', 'Chris Grosser', 'Success'),
            ('Success is the sum of small efforts repeated day in and day out.', 'Robert Collier', 'Success'),
            ('If you are not willing to risk the usual, you will have to settle for the ordinary.', 'Jim Rohn', 'Success'),

            # Resilience quotes
            ('The greatest glory in living lies not in never falling, but in rising every time we fall.', 'Nelson Mandela', 'Resilience'),
            ('It does not matter how slowly you go as long as you do not stop.', 'Confucius', 'Resilience'),
            ('Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time.', 'Thomas Edison', 'Resilience'),
            ('You may encounter many defeats, but you must not be defeated.', 'Maya Angelou', 'Resilience'),
            ('The oak fought the wind and was broken, the willow bent when it must and survived.', 'Robert Jordan', 'Resilience'),
            ('Rock bottom became the solid foundation on which I rebuilt my life.', 'J.K. Rowling', 'Resilience'),
            ('Fall seven times, stand up eight.', 'Japanese Proverb', 'Resilience'),
            ('Strength doesn\'t come from what you can do. It comes from overcoming the things you once thought you couldn\'t.', 'Rikki Rogers', 'Resilience'),
            ('The human capacity for burden is like bamboo - far more flexible than you\'d ever believe at first glance.', 'Jodi Picoult', 'Resilience'),
            ('It\'s not whether you get knocked down, it\'s whether you get up.', 'Vince Lombardi', 'Resilience'),
            ('What lies behind us and what lies before us are tiny matters compared to what lies within us.', 'Ralph Waldo Emerson', 'Resilience'),
            ('The bamboo that bends is stronger than the oak that resists.', 'Japanese Proverb', 'Resilience'),
            ('Perseverance is not a long race; it is many short races one after the other.', 'Walter Elliot', 'Resilience'),
            ('Character cannot be developed in ease and quiet. Only through experience of trial and suffering can the soul be strengthened.', 'Helen Keller', 'Resilience'),
            ('A river cuts through rock, not because of its power, but because of its persistence.', 'Jim Watkins', 'Resilience'),
            ('The strongest people are not those who show strength in front of us but those who win battles we know nothing about.', 'Jonathan Harnisch', 'Resilience'),
            ('Sometimes adversity is what you need to face in order to become successful.', 'Zig Ziglar', 'Resilience'),
            ('Out of suffering have emerged the strongest souls.', 'Kahlil Gibran', 'Resilience'),
            ('Resilience is accepting your new reality, even if it\'s less good than the one you had before.', 'Elizabeth Edwards', 'Resilience'),
            ('The world breaks everyone, and afterward, some are strong at the broken places.', 'Ernest Hemingway', 'Resilience'),

            # Growth quotes
            ('The only impossible journey is the one you never begin.', 'Tony Robbins', 'Growth'),
            ('In the middle of every difficulty lies opportunity.', 'Albert Einstein', 'Growth'),
            ('Learning is not attained by chance, it must be sought for with ardor and attended to with diligence.', 'Abigail Adams', 'Growth'),
            ('The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice.', 'Brian Herbert', 'Growth'),
            ('We cannot become what we want by remaining what we are.', 'Max Depree', 'Growth'),
            ('Growth is never by mere chance; it is the result of forces working together.', 'James Cash Penney', 'Growth'),
            ('The beautiful thing about learning is that nobody can take it away from you.', 'B.B. King', 'Growth'),
            ('Anyone who stops learning is old, whether at twenty or eighty.', 'Henry Ford', 'Growth'),
            ('Change is the end result of all true learning.', 'Leo Buscaglia', 'Growth'),
            ('The more that you read, the more things you will know. The more that you learn, the more places you\'ll go.', 'Dr. Seuss', 'Growth'),
            ('Intellectual growth should commence at birth and cease only at death.', 'Albert Einstein', 'Growth'),
            ('Continuous improvement is better than delayed perfection.', 'Mark Twain', 'Growth'),
            ('The mind is not a vessel to be filled, but a fire to be kindled.', 'Plutarch', 'Growth'),
            ('Every expert was once a beginner.', 'Helen Hayes', 'Growth'),
            ('The expert in anything was once a beginner.', 'Helen Hayes', 'Growth'),
            ('Personal growth is not a matter of learning new information but of unlearning old limits.', 'Alan Cohen', 'Growth'),
            ('Without continual growth and progress, words such as improvement, achievement, and success have no meaning.', 'Benjamin Franklin', 'Growth'),
            ('You are never too old to set another goal or to dream a new dream.', 'C.S. Lewis', 'Growth'),
            ('The only person you are destined to become is the person you decide to be.', 'Ralph Waldo Emerson', 'Growth'),
            ('Be not afraid of growing slowly; be afraid only of standing still.', 'Chinese Proverb', 'Growth'),

            # Courage quotes
            ('Courage is not the absence of fear, but rather the assessment that something else is more important than fear.', 'Franklin D. Roosevelt', 'Courage'),
            ('Have the courage to follow your heart and intuition. They somehow know what you truly want to become.', 'Steve Jobs', 'Courage'),
            ('It takes courage to grow up and become who you really are.', 'E.E. Cummings', 'Courage'),
            ('Courage is resistance to fear, mastery of fear, not absence of fear.', 'Mark Twain', 'Courage'),
            ('You can choose courage or you can choose comfort, but you cannot choose both.', 'Brene Brown', 'Courage'),
            ('Courage doesn\'t always roar. Sometimes courage is the quiet voice at the end of the day saying I will try again tomorrow.', 'Mary Anne Radmacher', 'Courage'),
            ('Life shrinks or expands in proportion to one\'s courage.', 'Anais Nin', 'Courage'),
            ('He who is not courageous enough to take risks will accomplish nothing in life.', 'Muhammad Ali', 'Courage'),
            ('Courage is being scared to death, but saddling up anyway.', 'John Wayne', 'Courage'),
            ('The brave man is not he who does not feel afraid, but he who conquers that fear.', 'Nelson Mandela', 'Courage'),
            ('With courage you will dare to take risks, have the strength to be compassionate, and the wisdom to be humble.', 'Keshavan Nair', 'Courage'),
            ('Courage is what it takes to stand up and speak; courage is also what it takes to sit down and listen.', 'Winston Churchill', 'Courage'),
            ('Fear is only as deep as the mind allows.', 'Japanese Proverb', 'Courage'),
            ('The only courage that matters is the kind that gets you from one moment to the next.', 'Mignon McLaughlin', 'Courage'),
            ('Courage is the most important of all the virtues because without courage, you can\'t practice any other virtue consistently.', 'Maya Angelou', 'Courage'),
            ('Be bold enough to use your voice, brave enough to listen to your heart, and strong enough to live the life you\'ve always imagined.', 'Unknown', 'Courage'),
            ('Courage is found in unlikely places.', 'J.R.R. Tolkien', 'Courage'),
            ('Real courage is when you know you\'re licked before you begin, but you begin anyway and see it through no matter what.', 'Harper Lee', 'Courage'),
            ('All our dreams can come true, if we have the courage to pursue them.', 'Walt Disney', 'Courage'),
            ('Do the thing you fear and the death of fear is certain.', 'Ralph Waldo Emerson', 'Courage'),

            # Mindfulness quotes
            ('The present moment is the only time over which we have dominion.', 'Thich Nhat Hanh', 'Mindfulness'),
            ('Mindfulness is a way of befriending ourselves and our experience.', 'Jon Kabat-Zinn', 'Mindfulness'),
            ('The best way to capture moments is to pay attention. This is how we cultivate mindfulness.', 'Jon Kabat-Zinn', 'Mindfulness'),
            ('Wherever you are, be all there.', 'Jim Elliot', 'Mindfulness'),
            ('Do every act of your life as though it were the very last act of your life.', 'Marcus Aurelius', 'Mindfulness'),
            ('The little things? The little moments? They aren\'t little.', 'Jon Kabat-Zinn', 'Mindfulness'),
            ('Paradise is not a place; it\'s a state of consciousness.', 'Sri Chinmoy', 'Mindfulness'),
            ('Mindfulness isn\'t difficult, we just need to remember to do it.', 'Sharon Salzberg', 'Mindfulness'),
            ('In today\'s rush, we all think too much - seek too much - want too much - and forget about the joy of just being.', 'Eckhart Tolle', 'Mindfulness'),
            ('Life is a dance. Mindfulness is witnessing that dance.', 'Amit Ray', 'Mindfulness'),
            ('The present moment is filled with joy and happiness. If you are attentive, you will see it.', 'Thich Nhat Hanh', 'Mindfulness'),
            ('Drink your tea slowly and reverently, as if it is the axis on which the world earth revolves.', 'Thich Nhat Hanh', 'Mindfulness'),
            ('Mindfulness means being awake. It means knowing what you are doing.', 'Jon Kabat-Zinn', 'Mindfulness'),
            ('Peace comes from within. Do not seek it without.', 'Buddha', 'Mindfulness'),
            ('The mind is everything. What you think you become.', 'Buddha', 'Mindfulness'),
            ('Be happy in the moment, that\'s enough. Each moment is all we need, not more.', 'Mother Teresa', 'Mindfulness'),
            ('Nature does not hurry, yet everything is accomplished.', 'Lao Tzu', 'Mindfulness'),
            ('Walk as if you are kissing the Earth with your feet.', 'Thich Nhat Hanh', 'Mindfulness'),
            ('Between stimulus and response there is a space. In that space is our power to choose our response.', 'Viktor Frankl', 'Mindfulness'),
            ('Realize deeply that the present moment is all you have. Make the NOW the primary focus of your life.', 'Eckhart Tolle', 'Mindfulness'),
        ]

        created_count = 0
        for text, author, category_name in quotes_data:
            quote, created = Quote.objects.get_or_create(
                text=text,
                author=author,
                defaults={'category': categories[category_name]}
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} quotes!'))
        self.stdout.write(self.style.SUCCESS(f'Total quotes in database: {Quote.objects.count()}'))
