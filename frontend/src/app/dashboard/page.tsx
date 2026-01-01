import { getSession } from '@/lib/auth';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await getSession();

  if (!session) {
    // This should be handled by middleware, but as a fallback
    redirect('/login');
  }

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center p-4">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <CardTitle className="text-3xl font-bold">Welcome back, {session.user.name}!</CardTitle>
          <CardDescription>
            This is your personalized dashboard.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p>Here&apos;s some information only a logged-in user can see.</p>
            <div className="p-4 rounded-lg bg-secondary">
              <p className="text-sm text-secondary-foreground">
                <span className="font-semibold">Your Email:</span> {session.user.email}
              </p>
              <p className="text-sm text-secondary-foreground">
                <span className="font-semibold">Your User ID:</span> {session.user.id}
              </p>
            </div>
            <p>
              Explore your account and manage your settings.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
