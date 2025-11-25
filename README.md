# AGDP Mobile App

Modern mobile application for AI-Generated Data Pipelines built with Expo and React Native.

## Features

- 🎨 Minimalistic, futuristic design with blue/purple gradients
- 📱 8 comprehensive screens for pipeline management
- ✨ Natural language pipeline generation
- 🔄 Real-time execution monitoring
- ⏰ Pipeline scheduling with cron expressions
- ⚙️ Configurable LLM settings

## Design System

### Colors
- **Primary**: Blue (#6366F1) and Purple (#A855F7) gradients
- **Background**: White (#FFFFFF)
- **Text**: Dark gray hierarchy for clarity
- **Status**: Green (success), Blue (info), Yellow (warning), Red (error)

### Typography
- **Headings**: System font, weights 600-700
- **Body**: 16px, line height 1.5
- **Consistent spacing**: 4, 8, 16, 24, 32, 48px scale

### Components
- **Cards**: Rounded (16px), subtle shadows
- **Buttons**: Gradient primary, flat secondary, outline variant
- **Inputs**: Rounded (12px), light gray background
- **Toggles**: Blue/purple accent colors

## Setup

1. Install dependencies:
```bash
cd agdp-mobile
npm install
```

2. Configure backend URL:
Edit `src/services/api.ts` and update `API_BASE_URL` to your backend URL.

3. Run the app:
```bash
npm start
```

Then scan the QR code with Expo Go app (iOS/Android) or press `w` for web.

## Screens

1. **Home Dashboard** - Quick actions and recent pipelines
2. **Create Pipeline** - Natural language prompt input with feature toggles
3. **Preview Pipeline** - Tabbed code view (Python, SQL, Soda, Prefect)
4. **Execution** - Step-by-step logs and output preview
5. **Schedule** - Cron expression configuration
6. **Pipeline List** - Browse all pipelines with status indicators
7. **Pipeline Detail** - Full pipeline information and actions
8. **Settings** - LLM model and storage configuration

## Navigation

- **Bottom Tabs**: Home, Pipelines, Create, Settings
- **Stack Navigation**: Nested screens within each tab
- **Deep Linking**: Direct navigation to pipeline details

## API Integration

The app connects to the AGDP FastAPI backend at `http://localhost:8000/api` by default.

Update the backend URL in `src/services/api.ts` before running.

## Development

```bash
# Start development server
npm start

# Run on Android
npm run android

# Run on iOS (macOS only)
npm run ios

# Run on web
npm run web
```

## Tech Stack

- **Framework**: Expo SDK 50
- **Language**: TypeScript
- **Navigation**: React Navigation 6
- **HTTP Client**: Axios
- **UI**: Custom design system with React Native components
